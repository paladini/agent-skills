---
name: oss-github-issue-to-release
description: Run an open-source GitHub issue from triage and validation through an approved plan, implementation, tests, documentation, pull request, CI, audit, and separately authorized merge or release. Use for issue-to-completion requests; use oss-pull-request-review for a contribution PR review that does not ask to implement a linked issue.
---

# Open-source GitHub issue to release

Orchestrate a **repeatable pipeline** for community and maintainer issues. This
skill is thin: it drives **phases**, **gates**, and a **persistent brief**; it
delegates deep work to existing skills and repo docs.

## Where files live

| What | Path |
|------|------|
| This skill (global) | `~/.agents/skills/oss-github-issue-to-release/` |
| Playbooks and templates | `reference/` under this skill directory |
| Per-issue state (working copy) | `<repo>/.agents/issues/<owner>-<repo>-<number>/` |
| Repo-specific overrides | `<repo>/.agents/skills/oss-github-issue-to-release.repo.md` if present |

Read repo overrides **before** phase 5 (implement). Repos may gitignore
`.agents/issues/`; the brief is for humans and agents, not necessarily shipped.

## User triggers

Parse the issue from a URL or `owner/repo#N`.

```text
oss-github-issue-to-release: https://github.com/org/repo/issues/42
```

**Default behavior:** run the **full pipeline** (validate -> plan -> implement -> docs -> changeset -> PR -> CI -> audit -> merge when you approve -> release when you approve -> verification report). There is no separate mode to choose - one skill, end to end.

Pause only at **GATE-PLAN**, **GATE-MERGE**, and **GATE-RELEASE**, or when you say to stop (e.g. “only plan this issue”, “stop after the PR is open”).

Approving **GATE-PLAN** continues straight through the issue comment in the repository's required language (English by default), implementation, commit, push, and pull request. Do not ask again before posting that comment or opening the PR, and do not offer to skip either step.

Resume without re-explaining:

```text
Continue oss-github-issue-to-release owner/repo#42
Approve GATE-PLAN
```

## Authority and safety

- Read `AGENTS.md`, `CONTRIBUTING.md`, and release docs in the target repo first.
- **Never** merge, push to someone else's branch without scope, tag, publish,
  or close issues manually without explicit user authorization.
- After **GATE-PLAN**, post the issue acknowledgment in the required language and open the
  fix PR on a branch of this repo. Those two steps are part of the pipeline.
- Use English for public GitHub text by default, unless repository policy or
  the user explicitly specifies another language (private chat may be any language).
- Credit external **issue reporters** separately from PR authors; never invent
  handles. First compare the reporter with the authenticated user and the
  repository's maintainer accounts. If the reporter is the user/maintainer,
  do not thank or credit them as an external contributor in the issue comment,
  PR body, changeset, or release notes. When the workflow requires an issue
  acknowledgment, keep it neutral and describe the reproduction or next step.
  Preserve explicit credit for genuine external contributors.
- External contributor PRs: push fixes to the **PR head branch**, not local
  `main` ahead of `origin/main`, when repo policy says so.

## Pipeline (phases and gates)

Execute in order. Update `brief.md` after every phase. **Stop only at
GATE-PLAN, GATE-MERGE, and GATE-RELEASE** until the user approves (or gave a
one-off “stop here” in the same request).

| Phase | Name | Gate |
|-------|------|------|
| 0 | Intake | - |
| 1 | Validate still relevant | GATE-VALIDATE (light; skip if obvious) |
| 2 | Classify and route playbook | - |
| 3 | Plan and scope (in/out) | **GATE-PLAN** |
| 4 | Issue acknowledgment | automatic after GATE-PLAN - post it |
| 5 | Implement + tests | - |
| 6 | Documentation (all required locales/surfaces) | - |
| 7 | Changeset / changelog prep | - |
| 8 | Commit and open PR (`Fixes #N`) | automatic after GATE-PLAN - commit, push, open PR |
| 9 | CI loop | - |
| 10 | Review comments / Bugbot | - |
| 11 | Pre-merge audit | **GATE-MERGE** (recommendation only) |
| 12 | Merge | **User must explicitly request** |
| 13 | Post-merge verification | - |
| 14 | Release | **GATE-RELEASE** + repo release skill |
| 15 | Public verification | report only |
| 16 | Consolidation report | - |

Detailed phase steps: [reference/playbooks.md](reference/playbooks.md).

Gate definitions: [reference/gates.md](reference/gates.md).

## Brief (single source of truth)

On phase 0, create or refresh:

`<repo>/.agents/issues/<owner>-<repo>-<number>/brief.md`

Use [reference/brief-template.md](reference/brief-template.md). Always record:

- issue URL, reporter, linked PRs, reported version vs current
- classification and playbook id
- scope in / out
- credit handles (reporter, contributor, reviewer if material)
- branch, PR URL, commands run and results
- gate log with timestamps or turn numbers
- verdict and next action

## Delegation (do not duplicate)

| Phase | Use |
|-------|-----|
| 11 | Follow a repository audit skill if available; otherwise audit against repository policy and save `audit-pre-merge.md` |
| 9-10 | `babysit`, `gh-fix-ci`, `gh-address-comments` when available and useful |
| 14 | Repo skill e.g. `release` or `RELEASING.md` when present |
| Vendor paths / APIs | Current official vendor docs first, not memory |

## Classification router

After phase 1, set playbook in the brief:

| Id | When |
|----|------|
| `community-bug` | Issue report + repro; you implement |
| `check-change` | Shared product model, public contract, compatibility rules, or fixtures |
| `external-pr` | Open PR from fork; you finish on head branch |
| `docs-only` | Guide/docs without behavior change |
| `maintainer-parse-gap` | Maintainer-authored schema parsing checklist; use the specialized playbook only when it fits the repo |
| `invalid-wontfix` | Not reproducible or out of product scope |

Playbook details: [reference/playbooks.md](reference/playbooks.md).
For schema-driven parsing backlog issues, consult [reference/maintainer-parse-gap-backlog.md](reference/maintainer-parse-gap-backlog.md) only when the issue and repository conventions fit that workflow.

## Final consolidation

Before recommending merge or release, output the report in
[reference/consolidation-report.md](reference/consolidation-report.md).
Do not equate green CI with released.
