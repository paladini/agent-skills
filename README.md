# Agent Skills

Reusable Agent Skills for researching, creating, validating, and publishing high-quality technical work.

## Skills

### DEV.to Publish Expert

[`devto-publish-expert`](skills/devto-publish-expert/) helps an AI agent research and write specialist DEV Community articles, select exactly four relevant tags, validate technical quality, and use a draft-first publishing workflow.

Key guarantees:

- quality and evidence before growth tactics;
- exactly four relevant DEV.to tags;
- no fabricated experience, benchmarks, or claims;
- deterministic Markdown validation;
- drafts by default and explicit approval before publication;
- correct handling of DEV temporary draft URLs.

## Install

Copy a skill directory into the skills location used by your agent:

```bash
git clone https://github.com/paladini/agent-skills.git
cp -R agent-skills/skills/devto-publish-expert ~/.codex/skills/
```

On Windows PowerShell:

```powershell
git clone https://github.com/paladini/agent-skills.git
Copy-Item -Recurse agent-skills\skills\devto-publish-expert $env:USERPROFILE\.codex\skills\
```

Restart the agent host after installation. Invoke the skill as `$devto-publish-expert` when explicit invocation is supported.

## Validate

Validate the skill structure with the Agent Skills validator, then run the bundled tests:

```bash
python path/to/skill-creator/scripts/quick_validate.py skills/devto-publish-expert
python -m unittest discover -s skills/devto-publish-expert/scripts -p "test_*.py"
```

## Contributing

Contributions are welcome. Keep skills concise, evidence-led, safe around external side effects, and compatible with progressive disclosure. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
