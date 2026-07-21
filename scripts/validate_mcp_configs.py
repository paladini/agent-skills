#!/usr/bin/env python3
"""Validate committed MCP examples and reject likely credentials."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = ROOT / "mcp-configs"
PLACEHOLDER = "REPLACE_WITH_LOCAL_SECRET"
SUSPICIOUS = [
    re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\b(?:api[_-]?key|token|secret|password)\s*[=:]\s*[\"']?(?!REPLACE_)[A-Za-z0-9_./+-]{16,}", re.I),
    re.compile(r"\b(?:li_at|JSESSIONID)\s*[=:]", re.I),
]


def validate() -> list[str]:
    errors: list[str] = []
    json_files = sorted(CONFIG_ROOT.rglob("*.json.example"))
    toml_files = sorted(CONFIG_ROOT.rglob("*.toml.example"))

    if len(json_files) != 3 or len(toml_files) != 3:
        errors.append("expected three JSON and three TOML MCP examples")

    for path in json_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data.get("mcpServers"), dict):
                errors.append(f"{path}: missing mcpServers object")
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: {exc}")

    for path in toml_files:
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data.get("mcp_servers"), dict):
                errors.append(f"{path}: missing mcp_servers table")
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"{path}: {exc}")

    for path in sorted(CONFIG_ROOT.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in SUSPICIOUS:
            if pattern.search(text):
                errors.append(f"{path}: possible committed credential")
        if path.name == ".env.example" and PLACEHOLDER not in text:
            errors.append(f"{path}: expected secret placeholder")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: sanitized MCP configurations are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
