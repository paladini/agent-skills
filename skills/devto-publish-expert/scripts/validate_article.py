#!/usr/bin/env python3
"""Validate a DEV.to Markdown draft without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TAG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FENCE_RE = re.compile(r"^```([^\s`]*)", re.MULTILINE)


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unterminated YAML front matter")

    metadata: dict[str, str] = {}
    for number, raw_line in enumerate(text[4:end].splitlines(), start=2):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid front matter on line {number}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"\'')
    return metadata, text[end + 5 :]


def parse_tags(raw: str) -> list[str]:
    value = raw.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [part.strip().strip('"\'').lower() for part in value.split(",") if part.strip()]


def validate(path: Path, allow_published: bool = False) -> list[str]:
    errors: list[str] = []
    try:
        metadata, body = parse_front_matter(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        return [str(exc)]

    title = metadata.get("title", "")
    description = metadata.get("description", "")
    published = metadata.get("published", "").lower()
    tags = parse_tags(metadata.get("tags", ""))

    if not 20 <= len(title) <= 128:
        errors.append("title must contain 20-128 characters")
    if not 50 <= len(description) <= 160:
        errors.append("description must contain 50-160 characters")
    if published not in {"true", "false"}:
        errors.append("published must be true or false")
    elif published == "true" and not allow_published:
        errors.append("published must be false unless --allow-published is explicit")
    if len(tags) != 4:
        errors.append("exactly four tags are required")
    if len(set(tags)) != len(tags):
        errors.append("tags must be unique")
    invalid_tags = [tag for tag in tags if not TAG_RE.fullmatch(tag)]
    if invalid_tags:
        errors.append(f"invalid tag format: {', '.join(invalid_tags)}")

    words = re.findall(r"\b[\w'-]+\b", body, flags=re.UNICODE)
    if len(words) < 700:
        errors.append("article body must contain at least 700 words")
    if len(re.findall(r"^##\s+\S", body, flags=re.MULTILINE)) < 3:
        errors.append("article needs at least three level-two sections")
    unlabeled = [match.group(0) for match in FENCE_RE.finditer(body) if not match.group(1)]
    if unlabeled:
        errors.append("all fenced code blocks must include a language identifier")
    if re.search(r"(?:api[_ -]?key|token|secret)\s*[:=]\s*['\"][A-Za-z0-9_-]{16,}", body, re.I):
        errors.append("possible secret detected in article body")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path)
    parser.add_argument(
        "--allow-published",
        action="store_true",
        help="allow published: true after explicit publication approval",
    )
    args = parser.parse_args()
    errors = validate(args.article, args.allow_published)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {args.article} is a valid DEV.to article")
    return 0


if __name__ == "__main__":
    sys.exit(main())
