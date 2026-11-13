#!/usr/bin/env python3
"""Safely inspect and append to a DEV publication history (standard library only)."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import uuid

MAX_BYTES = 10 * 1024 * 1024
MAX_FIELD = 16 * 1024
MANAGED = 'publication-history.json.managed-v2-'


class HistoryError(ValueError):
    pass


def decode(raw):
    if len(raw) > MAX_BYTES:
        raise HistoryError('history exceeds 10 MiB')
    try:
        data = json.loads(raw.decode('utf-8-sig'))
    except (UnicodeError, ValueError) as exc:
        raise HistoryError(f'invalid UTF-8 JSON: {exc}') from exc
    if not isinstance(data, dict) or not all(isinstance(data.get(k), list) for k in ('articles', 'runs')):
        raise HistoryError('history must contain articles and runs arrays')
    if not all(isinstance(x, dict) for key in ('articles', 'runs') for x in data[key]):
        raise HistoryError('history entries must be objects')
    for record in data['articles'] + data['runs']:
        title = record.get('title')
        if isinstance(title, str) and (len(title) > 1000 or '\ufffd' in title):
            raise HistoryError('corrupt or oversized title')
    return data


def read(path):
    if path.stat().st_size > MAX_BYTES:
        raise HistoryError('history exceeds 10 MiB')
    raw = path.read_bytes()
    return raw, decode(raw)


def ident(record):
    values = [record[k] for k in ('devtoArticleId', 'articleId') if record.get(k) is not None]
    normalized = []
    for value in values:
        if isinstance(value, bool) or not str(value).isdigit() or int(value) <= 0:
            raise HistoryError('invalid article ID')
        normalized.append(int(value))
    if len(set(normalized)) > 1:
        raise HistoryError('conflicting article IDs')
    return normalized[0] if normalized else None


def check_new(value, key=''):
    if isinstance(value, str):
        if len(value.encode('utf-8')) > MAX_FIELD or '\ufffd' in value:
            raise HistoryError(f'oversized or corrupt field: {key}')
    elif isinstance(value, dict):
        for k, v in value.items():
            if k.lower() in {'body', 'body_markdown', 'payload', 'tool_response'}:
                raise HistoryError(f'prohibited field: {k}')
            check_new(v, k)
    elif isinstance(value, list):
        for v in value:
            check_new(v, key)


def save(path, original, data):
    payload = (json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
    decode(payload)
    if len(payload) > len(original) * 2 + 65536:
        raise HistoryError('history grew unexpectedly; refusing write')
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + '.tmp-', delete=False) as f:
            temp_name = f.name
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        if decode(Path(temp_name).read_bytes()) != data:
            raise HistoryError('temporary file validation failed')
        if path.read_bytes() != original:
            raise HistoryError('history changed concurrently')
        backup = path.parent / (MANAGED + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ-') + uuid.uuid4().hex + '.bak')
        with backup.open('xb') as f:
            f.write(original)
            f.flush()
            os.fsync(f.fileno())
        if backup.read_bytes() != original:
            raise HistoryError('backup verification failed')
        decode(backup.read_bytes())
        os.replace(temp_name, path)
        temp_name = None
        if path.read_bytes() != payload:
            raise HistoryError('post-write verification failed; recover from ' + str(backup))
        backups = sorted(path.parent.glob(MANAGED + '*.bak'), key=lambda p: p.name, reverse=True)
        for old in backups[3:]:
            old.unlink()
        return {'beforeBytes': len(original), 'afterBytes': len(payload), 'backup': str(backup)}
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def append_locked(path, update):
    if not isinstance(update, dict) or set(update) - {'articles', 'runs', 'lastReconciledAt'}:
        raise HistoryError('update must contain only articles, runs, lastReconciledAt')
    raw, data = read(path)
    for key in ('articles', 'runs'):
        entries = update.get(key, [])
        if not isinstance(entries, list) or not all(isinstance(x, dict) for x in entries):
            raise HistoryError(f'{key} update must be an array of objects')
        for incoming in entries:
            check_new(incoming)
            record = dict(incoming)
            if key == 'articles':
                article_id = ident(record)
                if not article_id:
                    raise HistoryError('new article requires an ID')
                url = record.get('devtoUrl') or record.get('url')
                if record.get('devtoUrl') and record.get('url') and record['devtoUrl'] != record['url']:
                    raise HistoryError('conflicting article URLs')
                if record.get('source') == 'automation' and (not record.get('publishedOn') or not isinstance(url, str) or not url.startswith('https://dev.to/')):
                    raise HistoryError('automated articles require publishedOn and DEV URL')
                record['devtoArticleId'] = article_id
                if url:
                    record['devtoUrl'] = url
                matches = [x for x in data[key] if ident(x) == article_id]
                if matches:
                    existing = matches[0]
                    for field, value in record.items():
                        if field in existing and existing[field] != value:
                            raise HistoryError(f'existing article {article_id} differs in {field}; reconcile manually')
                    existing.update(record)
                    continue
            else:
                if not isinstance(record.get('runId'), str) or not record['runId']:
                    raise HistoryError('new run requires unique runId')
                matches = [x for x in data[key] if x.get('runId') == record['runId']]
                if matches:
                    if matches[0] != record:
                        raise HistoryError('runId already exists with different content')
                    continue
            data[key].append(record)
    if 'lastReconciledAt' in update:
        check_new(update['lastReconciledAt'], 'lastReconciledAt')
        if not isinstance(update['lastReconciledAt'], str):
            raise HistoryError('lastReconciledAt must be a string')
        data['lastReconciledAt'] = update['lastReconciledAt']
    result = save(path, raw, data)
    return {**result, 'articles': len(data['articles']), 'runs': len(data['runs'])}


def append(path, update):
    lock = path.with_name(path.name + '.write.lock')
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise HistoryError('history write lock exists; investigate before removing it') from exc
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(str(os.getpid()))
        return append_locked(path, update)
    finally:
        lock.unlink()


def repo(value):
    if not isinstance(value, str):
        raise HistoryError('repository name must be owner/name')
    value = value.strip().lower().removesuffix('.git')
    if len(value.split('/')) != 2 or not all(value.split('/')):
        raise HistoryError('repository name must be owner/name')
    return value


def rotation(data, inventory, candidate=None):
    if not isinstance(inventory, dict) or inventory.get('inventoryComplete') is not True or inventory.get('articlesComplete') is not True:
        raise HistoryError('complete GitHub inventory and DEV article reconciliation are required')
    if inventory.get('unresolvedArticles') != []:
        raise HistoryError('unresolved article-to-repository mappings require review')
    if not isinstance(inventory.get('eligibleRepositories'), list) or not isinstance(inventory.get('coveredRepositories'), list):
        raise HistoryError('eligibleRepositories and coveredRepositories arrays required')
    eligible = {repo(x) for x in inventory['eligibleRepositories']}
    covered = {repo(x) for x in inventory['coveredRepositories']}
    for record in data['articles']:
        if record.get('repository'):
            covered.add(repo(record['repository']))
    unseen = sorted(eligible - covered)
    result = {'eligibleCount': len(eligible), 'uncoveredCount': len(unseen), 'uncoveredRepositories': unseen}
    if candidate:
        chosen = repo(candidate)
        if chosen not in eligible:
            raise HistoryError('candidate is not eligible')
        if unseen and chosen not in unseen:
            raise HistoryError('covered candidate refused while uncovered eligible repositories exist')
        result['candidate'] = chosen
        result['candidatePreviouslyCovered'] = chosen in covered
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', required=True, type=Path)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('check')
    add = commands.add_parser('append')
    add.add_argument('--input', required=True, type=Path)
    rotate = commands.add_parser('rotation')
    rotate.add_argument('--inventory', required=True, type=Path)
    rotate.add_argument('--candidate')
    args = parser.parse_args()
    try:
        if args.command == 'append':
            update = json.loads(args.input.read_text(encoding='utf-8-sig'))
            result = append(args.state, update)
        else:
            raw, state = read(args.state)
            if args.command == 'rotation':
                inventory = json.loads(args.inventory.read_text(encoding='utf-8-sig'))
                result = rotation(state, inventory, args.candidate)
            else:
                result = {'bytes': len(raw), 'articles': len(state['articles']), 'runs': len(state['runs']), 'sha256': hashlib.sha256(raw).hexdigest()}
        print(json.dumps(result, ensure_ascii=False))
    except (OSError, ValueError, TypeError) as exc:
        print(f'publication history error: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
