# Playbooks

## Phase 0 - Intake

1. `gh issue view <url> --json title,body,author,labels,comments,number,state`
2. Search for linked PRs (`Fixes #`, `Closes #`, cross-refs in body).
3. Create brief from [brief-template.md](brief-template.md).
4. Read repository `AGENTS.md`, `CONTRIBUTING.md`, release docs, and any other project-level agent instructions that apply.

## Phase 1 - Validate

1. Compare reported version to current (tags, `package.json`, releases).
2. Reproduce minimally or cite code path proving bug/feature gap still exists.
3. For tool integration issues: consult **current official docs**; record URLs in brief.
4. If invalid/duplicate: playbook `invalid-wontfix`, draft a response in the repository's required language (English by default), and stop at GATE-VALIDATE.

## Phase 2 - Classify

Set playbook id in brief (see SKILL.md router).

### `community-bug`

Reporter opened issue; you implement. Credit an external reporter in the changeset/PR even if they did not open the PR. Compare the reporter with the authenticated user and repository maintainers; use neutral acknowledgment and no self-credit when the reporter is the user or a maintainer. Follow repository credit policy.

### `check-change`

Issue changes a product model, public contract, or scoring system. Before coding, confirm the issue and repository policy establish the required maintainer agreement. Sync all required implementation, docs, fixtures, and compatibility surfaces. Use a focused audit when one is available.

### `external-pr`

Existing fork PR that implements this issue. Compare PR base/head; follow repository policy for proposing fixes on the contributor's branch; write public review comments in the repository's required language; credit the PR author and issue reporter when they differ and are external contributors. For review-only requests without issue implementation, use `oss-pull-request-review`.

### `docs-only`

No behavior change. Run docs build and locale parity checks when the repository requires them.

### `invalid-wontfix`

Document why; use the repository's required language for any response; do not open a drive-by PR.

### `maintainer-parse-gap`

Use only for a maintainer-authored issue that already defines a narrow schema or parsing checklist. Read [maintainer-parse-gap-backlog.md](maintainer-parse-gap-backlog.md) as optional guidance, then validate every branch, version, fixture, and release assumption against the target repository's own policy.

## Phase 3 - Plan

1. Smallest correct diff; explicit in/out (matches public issue comment later).
2. List files and tests; note snapshot/golden updates.
3. Write `plan.md` snapshot; stop at **GATE-PLAN**.

## Phase 4 - Issue acknowledgment (public)

After GATE-PLAN, post the comment in the repository's required language. Confirm validity on the current version, summarize the planned fix and **out of scope**, and thank the reporter only when they are an external contributor. If the reporter is the authenticated user or a maintainer account, keep the required acknowledgment neutral and do not thank them. Do not wait for a separate approval and do not offer to skip the post.

## Phase 5 - Implement

Follow repository invariants (architecture, dependencies, API stability, supported platforms, and compatibility). No scope creep.

## Phase 6 - Documentation

Update every surface the repo requires (README, guides, locales, API references, metrics, and migration notes). Preserve stable public anchors unless intentionally migrating them.

## Phase 7 - Release metadata

User-facing repos: prepare a changeset/changelog entry in the required language and explicitly credit external reporters/contributors when repository policy requires it. Never add a self-thank-you or self-credit for the authenticated user or a maintainer who reported the issue.

## Phase 8 - Commit and PR

1. Branch name: `fix/issue-<N>-<short-slug>` or match repo convention. Branch from current `origin/main`, not from whatever feature branch happens to be checked out.
2. PR body in the repository's required language (English by default): Summary, Test plan, `Fixes #N`, and any required external-contributor credits. Do not credit the authenticated user or a maintainer as the issue reporter.
3. Commit, push, and open the PR. This is automatic after GATE-PLAN. Do not wait for a separate approval.

## Phase 9 - CI loop

`gh pr checks`. On failure: `gh-fix-ci` or fix in scope. On unrelated main drift: merge/rebase base if repo policy allows. Use `babysit` for sustained loop.

## Phase 10 - Review

Unresolved review threads: `gh-address-comments`. Bugbot: validate before fixing.

## Phase 11 - Pre-merge audit

Use the repository's PR or release audit skill if available. Otherwise, audit against its required checks, compatibility policy, and release metadata. Write `audit-pre-merge.md`, present the consolidation report, and stop at **GATE-MERGE** (recommendation only).

## Phase 12 - Merge

Only when user explicitly asks. Use `gh pr merge` per repo preference.

## Phase 13 - Post-merge

Confirm issue closed via linkage; main CI; no accidental amend of release commits.

## Phase 14 - Release

After merge, use `oss-release-and-deploy` for read-only deployment checks and release coordination. When **GATE-RELEASE** is approved, follow the repo release skill / `RELEASING.md` through that coordinator. Never publish without explicit authorization. A release-preparation PR has its own **GATE-MERGE**; approval to release the original change does not approve merging that second PR.

## Phase 15 - Public verification

Use `oss-release-and-deploy` to check each applicable registry, GitHub Release, tag, marketplace listing, and deployed site independently; report URLs, versions, and any remaining manual steps.

## Phase 16 - Consolidation

Emit [consolidation-report.md](consolidation-report.md) format.
