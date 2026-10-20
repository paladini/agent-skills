# Consolidation report template

Copy this structure into chat (and optionally into `brief.md`) before
recommending merge or release.

```markdown
## Open-source GitHub issue to release - consolidation

**Issue:** <owner>/<repo>#<N> - <title>
**PR:** <url or none>
**Playbook:** <id>
**Verdict:** ready for merge | ready for release | blocked - <reason>

### What changed (one paragraph)

### Scope honored

- In: …
- Out (documented): …

### Credits

- Reporter: @…
- Contributor: @…
- Changeset / release note credit: verified | gap - ...

### Evidence

- Local checks: …
- CI: …
- Pre-merge audit (pr-release-audit): …

### Public communication

- Issue comment (required language): posted | draft only | skipped
- Fixes #N on PR: yes | no

### Release (if applicable)

- Changeset: …
- Release prepare: not started | in progress | done
- Public registries/site: not verified | verified - ...

### Delivery state

| Surface | State | Evidence / URL |
|---------|-------|---------------|
| Source PR merge | pending | |
| Release | not applicable | |
| Registry / marketplace artifacts | not applicable | |
| Documentation deployment | not applicable | |
| Public verification | pending | |

### Your explicit OK still needed

- [ ] Merge
- [ ] Merge release-preparation PR (if required; separate approval)
- [ ] Release
- [ ] None - user asked to stop before merge/release

### Follow-ups (optional)

-
```

Never state that a version is public until independently verified (npm, GitHub
Release, Pages, etc.).
