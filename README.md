# Agent Skills

Reusable Agent Skills for researching, creating, validating, and publishing high-quality technical work.

The repository also stores sanitized [MCP server configurations](mcp-configs/) for restoring publishing workflows without committing real credentials or browser sessions.

## Skills

### OSS GitHub Issue to Release

[`oss-github-issue-to-release`](skills/oss-github-issue-to-release/) runs an open-source issue through validation, planning, implementation, pull request, CI, audit, and separately approved merge or release.

### OSS Pull Request Review

[`oss-pull-request-review`](skills/oss-pull-request-review/) evaluates contributor pull requests for demonstrated need, fit with product direction, technical quality, and consistency across related languages, tools, and versions.

### PR and Release Audit

[`pr-release-audit`](skills/pr-release-audit/) complements OSS contribution review with deeper merge and release checks, including current vendor contracts, documentation and site parity, release metadata, and explicit contributor credit. Use it alongside `oss-pull-request-review` when an external contribution is a candidate for merge or changes release-facing files.

### DEV.to Publish Expert

[`devto-publish-expert`](skills/devto-publish-expert/) helps an AI agent research and write specialist DEV Community articles, select exactly four relevant tags, validate technical quality, and use a draft-first publishing workflow.

Key guarantees:

- quality and evidence before growth tactics;
- exactly four relevant DEV.to tags;
- no fabricated experience, benchmarks, or claims;
- deterministic Markdown validation;
- drafts by default and explicit approval before publication;
- correct handling of DEV temporary draft URLs.

## Keep Global Skills in Sync

Use this repository as the canonical source for your personal skills. Clone it once on each computer, pull before working, and link its skill folders into your agent's global skill directory. Editing a linked skill edits the tracked source in this clone.

On Windows PowerShell, the default links skills into the shared user-level `.agents/skills` directory used by Codex and compatible agents. Use `-Agent all` to also link Claude Code:

```powershell
New-Item -ItemType Directory -Force "$HOME\Developer" | Out-Null
git clone https://github.com/paladini/agent-skills.git "$HOME\Developer\agent-skills"
Set-Location "$HOME\Developer\agent-skills"
git pull
.\scripts\link-global-skills.ps1 -Agent codex
```

On macOS or Linux (use the PowerShell script on Windows):

```bash
mkdir -p "$HOME/Developer"
git clone https://github.com/paladini/agent-skills.git "$HOME/Developer/agent-skills"
cd "$HOME/Developer/agent-skills"
git pull
./scripts/link-global-skills.sh --agent codex
```

Codex also scans the legacy `$CODEX_HOME/skills` location. Use `.agents/skills` as the shared source here; the installer preserves a same-named legacy skill and reports the conflict instead of creating a duplicate. See [Codex skill discovery roots](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs#L914-L935). Choose `all` to link the shared directory and Claude Code, or pass one or more custom skill roots with `-TargetRoot` (PowerShell) or `--target-root` (shell). Run the link command after adding a skill. When renaming or removing one, remove its old link manually after confirming it points into this repository; the installer does not prune links. To link just one skill, use `-SkillName <name>` or `--skill <name>`. Existing skill directories are never overwritten; resolve a reported conflict manually after inspecting and preserving its contents.

After editing a skill, inspect `git diff`, then commit and push the change. On another computer, run `git pull`; existing links immediately use the updated files. Git does not upload local edits automatically, so push each change you want backed up on GitHub. Do not commit credentials, private prompts, or personal data.

## Validate

Validate the skill structure with the Agent Skills validator, run the bundled tests, and check the global link scripts:

```bash
python path/to/skill-creator/scripts/quick_validate.py skills/devto-publish-expert
python -m unittest discover -s skills/devto-publish-expert/scripts -p "test_*.py"
python scripts/validate_mcp_configs.py
python path/to/skill-creator/scripts/quick_validate.py skills/oss-github-issue-to-release
python path/to/skill-creator/scripts/quick_validate.py skills/oss-pull-request-review
python -m unittest discover -s scripts -p "test_link_global_skills.py"
```

## Contributing

Contributions are welcome. Keep skills concise, evidence-led, safe around external side effects, and compatible with progressive disclosure. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT license - see [LICENSE](LICENSE).
