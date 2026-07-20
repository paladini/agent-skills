#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path

from validate_article import validate


def article(*, tags: str = "mcp, tutorial, typescript, devto", published: str = "false") -> str:
    body = " ".join(["Useful technical explanation"] * 240)
    return f'''---
title: "Build a Safe DEV.to Publishing Workflow"
published: {published}
description: "Create and validate specialist technical tutorials before saving them safely as DEV.to drafts."
tags: {tags}
---

## Problem

{body}

## Implementation

{body}

## Verification

{body}
'''


class ValidatorTests(unittest.TestCase):
    def write(self, content: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "article.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_draft(self) -> None:
        self.assertEqual(validate(self.write(article())), [])

    def test_requires_four_tags(self) -> None:
        errors = validate(self.write(article(tags="mcp, tutorial, typescript")))
        self.assertIn("exactly four tags are required", errors)

    def test_blocks_publishing_by_default(self) -> None:
        errors = validate(self.write(article(published="true")))
        self.assertTrue(any("--allow-published" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
