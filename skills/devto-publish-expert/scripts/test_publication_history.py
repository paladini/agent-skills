import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import publication_history as history


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'publication-history.json'
        self.initial = {'articles': [{'articleId': 5, 'repository': 'Owner/Old', 'title': 'Ação — 🚀'}], 'runs': [], 'extra': {'retained': True}}
        self.path.write_text(json.dumps(self.initial, ensure_ascii=False), encoding='utf-8')

    def test_unicode_survives_repeated_writes_and_backups_are_bounded(self):
        for i in range(5):
            history.append(self.path, {'runs': [{'runId': str(i), 'title': 'Ação — 🚀'}]})
        raw, data = history.read(self.path)
        self.assertEqual(data['articles'], self.initial['articles'])
        self.assertEqual(data['extra'], self.initial['extra'])
        self.assertEqual(len(data['runs']), 5)
        self.assertIn('Ação — 🚀', raw.decode('utf-8'))
        backups = list(self.path.parent.glob(history.MANAGED + '*.bak'))
        self.assertEqual(len(backups), 3)
        for backup in backups:
            history.read(backup)

    def test_legacy_identity_enrichment_and_idempotency(self):
        update = {'articles': [{'devtoArticleId': 5, 'url': 'https://dev.to/u/post', 'source': 'automation', 'publishedOn': '2026-11-13'}], 'runs': [{'runId': 'one'}]}
        history.append(self.path, update)
        history.append(self.path, update)
        _, data = history.read(self.path)
        self.assertEqual(len(data['articles']), 1)
        self.assertEqual(data['articles'][0]['devtoUrl'], 'https://dev.to/u/post')
        self.assertEqual(len(data['runs']), 1)

    def test_collision_and_bad_new_fields_leave_original_unchanged(self):
        for update in ({'articles': [{'articleId': 5, 'title': 'different'}]},
                       {'runs': [{'runId': 'x', 'body_markdown': 'no'}]},
                       {'runs': [{'runId': 'x', 'title': 'x' * 20000}]},
                       {'articles': [{'articleId': 2, 'source': 'automation'}]}):
            old = self.path.read_bytes()
            with self.assertRaises(history.HistoryError):
                history.append(self.path, update)
            self.assertEqual(self.path.read_bytes(), old)

    def test_invalid_or_oversized_state_never_copied(self):
        for raw in (b'{', b'{"articles":[],"runs":[]}\xff', b' ' * (history.MAX_BYTES + 1)):
            self.path.write_bytes(raw)
            with self.assertRaises(history.HistoryError):
                history.append(self.path, {'runs': [{'runId': 'x'}]})
            self.assertEqual(self.path.read_bytes(), raw)
            self.assertFalse(list(self.path.parent.glob(history.MANAGED + '*.bak')))

    def test_failed_replace_keeps_original_and_verified_backup(self):
        old = self.path.read_bytes()
        with patch.object(history.os, 'replace', side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):
                history.append(self.path, {'runs': [{'runId': 'x'}]})
        self.assertEqual(self.path.read_bytes(), old)
        self.assertEqual(list(self.path.parent.glob(history.MANAGED + '*.bak'))[0].read_bytes(), old)
        self.assertFalse(list(self.path.parent.glob('*.tmp-*')))

    def test_growth_guard_and_legacy_backups(self):
        legacy = self.path.parent / 'publication-history.json.bak-legacy'
        legacy.write_bytes(b'legacy evidence')
        old = self.path.read_bytes()
        with self.assertRaises(history.HistoryError):
            history.append(self.path, {'runs': [{'runId': str(i), 'details': 'x' * 10000} for i in range(8)]})
        self.assertEqual(self.path.read_bytes(), old)
        history.append(self.path, {'runs': [{'runId': 'safe'}]})
        self.assertEqual(legacy.read_bytes(), b'legacy evidence')

    def test_missing_rotation_fields_fail_closed(self):
        for inventory in ({}, {'inventoryComplete': True, 'articlesComplete': True, 'unresolvedArticles': []},
                          {'inventoryComplete': True, 'articlesComplete': True, 'eligibleRepositories': [], 'coveredRepositories': []}):
            with self.assertRaises(history.HistoryError):
                history.rotation(self.initial, inventory)

    def test_lock_blocks_another_writer(self):
        lock = self.path.with_name(self.path.name + '.write.lock')
        lock.write_text('other', encoding='utf-8')
        with self.assertRaises(history.HistoryError):
            history.append(self.path, {'runs': [{'runId': 'x'}]})
        self.assertEqual(lock.read_text(), 'other')

    def test_rotation_requires_complete_data_and_prioritizes_uncovered(self):
        inventory = {'inventoryComplete': True, 'articlesComplete': True, 'unresolvedArticles': [], 'eligibleRepositories': ['owner/old', 'Owner/New'], 'coveredRepositories': []}
        result = history.rotation(self.initial, inventory, 'owner/new')
        self.assertEqual(result['uncoveredRepositories'], ['owner/new'])
        with self.assertRaises(history.HistoryError):
            history.rotation(self.initial, inventory, 'owner/old')
        for changes in ({'articlesComplete': False}, {'inventoryComplete': False}, {'unresolvedArticles': [42]}):
            with self.assertRaises(history.HistoryError):
                history.rotation(self.initial, {**inventory, **changes})
        inventory['eligibleRepositories'] = ['owner/old']
        self.assertTrue(history.rotation(self.initial, inventory, 'owner/old')['candidatePreviouslyCovered'])


if __name__ == '__main__':
    unittest.main()
