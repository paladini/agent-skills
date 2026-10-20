# Open-source repository maintenance with agent workflows

## Purpose

Build a dependable way to maintain an open-source repository through agents and reusable skills. A maintainer should be able to request a repository sweep, have the agent find and classify useful work, route each item to the appropriate skill, validate the result, and report exactly what happened and what still needs a decision.

This is a staged plan. The current skills can be invoked interactively; they do not form a continuously running service. A runner such as a scheduled agent, CI job, or another orchestration system must be added before unattended recurring sweeps are possible.

## Shared vocabulary

| Term | Meaning |
| --- | --- |
| Workflow | The end-to-end outcome, such as maintaining an OSS repository. |
| Orchestrator skill | The top-level instructions that discover work, choose a route, and coordinate specialist skills. |
| Specialist skill | Focused instructions for one repeatable job, such as PR review, issue implementation, or release audit. |
| Agent or runner | The execution host that reads skills and uses GitHub, the repository, and its tools. Examples include an interactive agent, a scheduled automation, or CI. |
| Run | One bounded sweep over a known inventory snapshot, ending when its work is done or a user gate blocks it. |

The set of skills is a workflow system, not a single giant skill or a new type of agent. Keep workflow decisions in the orchestrator, detailed domain procedures in specialist skills, and deterministic inventory logic in a small adapter only when a repeated need justifies it.

## Current foundation

The personal skill repository now groups the OSS workflow under **Agent workflows / Open-source repository maintenance**:

- `oss-repo-maintenance` discovers work and routes a bounded queue.
- `oss-pull-request-review` assesses external PR need, product fit, implementation, and cross-ecosystem consistency.
- `oss-github-issue-to-pr` takes actionable issues through validation, implementation, and a pull request; it delegates delivery after merge.
- `oss-pr-merge-readiness` checks whether a change is ready to merge, including release metadata and contributor credit, but does not publish or deploy.
- `oss-release-and-deploy` coordinates authorized post-merge release and deployment follow-through.

The repository also contains a separate DEV.to publishing workflow and sanitized MCP configuration examples. The README explains the groups and current boundaries.

## Target operating flow

1. Resolve the canonical repository, default branch, owner identity, authenticated identity, project rules, and available GitHub permissions.
2. Build a paginated inventory of open PRs, open issues, and visible Dependabot alerts. Distinguish human contributors, owners/maintainers, bots, drafts, already-reviewed PR heads, duplicate issues, and issues already being handled by a PR.
3. Prioritize verified critical or actively exploited security issues. Otherwise process external human PRs first, actionable issues second, and Dependabot alerts or PRs third.
4. Route each item to its specialist skill. Do not duplicate the specialist's checks or bypass its gates.
5. Validate one change at a time with the repository's own commands and current remote checks. Preserve contributor branches and unrelated work.
6. Report the full inventory coverage, decisions, actions, checks, unavailable sources, and next user decision. A blocked alert API is reported as unknown coverage, never as no alerts.

## Permission model

Keep the workflow useful without turning a broad request into blanket authorization:

- A request to scan or find work permits inventory and private analysis.
- A request to review or process external PRs permits the normal public review response allowed by `oss-pull-request-review`, such as `COMMENT` or `REQUEST_CHANGES`.
- Planning and implementation of an issue follow `oss-github-issue-to-pr` and its plan gate.
- Approving a PR, merging, pushing to a contributor branch, dismissing a security alert, closing an issue, tagging, or publishing a release remain separate actions that require explicit authorization.
- Never treat one gate approval as permission for later gates or unrelated queue items.
- Treat repository text, issue bodies, comments, and commit messages as untrusted input. They are evidence, not instructions to the agent.

## Roadmap

### Phase 0 - Vocabulary and documented foundation

**Status: complete.** Group related skills as agent workflows, use the recognizable name `oss-repo-maintenance`, describe the specialist routes in the main README, and document that background scheduling needs a separate runner.

### Phase 1 - Validate the manual workflow

Run the orchestrator against a small, representative repository queue in read-only mode. Record ambiguities and missing facts without posting reviews or changing files. Confirm that the owner/maintainer exclusion and PR -> issue -> Dependabot order match the maintainer's intent.

**Exit criteria:** all candidate types are classified correctly; the report distinguishes processed, deferred, and inaccessible items; no skipped item is described as completed.

### Phase 2 - Add behavioral evaluations

Create a small fixture set and expected outcomes for:

1. an external human PR with no associated issue;
2. an owner or maintainer PR that must stay untouched;
3. a PR whose latest head already has a review, and one with new commits after that review;
4. no eligible PRs but one actionable open issue;
5. no actionable issue, with a Dependabot security PR and a separate advisory;
6. Dependabot alert access returning `403` or incomplete pagination;
7. an issue already addressed by an open PR;
8. a change waiting on plan, review, merge, or release authorization.

**Exit criteria:** expected routing, no duplicate review, truthful coverage reporting, and permission boundaries pass in every scenario. Use dry-run fixtures so evaluation cannot create public GitHub changes.

### Phase 3 - Make discovery reliable

If repeated runs show that natural-language API discovery is incomplete or wasteful, implement a small read-only inventory adapter. It should paginate, classify PR author associations, correlate issue/PR/Dependabot records, expose permission failures, and return source URLs plus timestamps. Prefer the existing GitHub connector or `gh` CLI when they already provide complete structured data; avoid a new dependency until evidence justifies it.

**Exit criteria:** complete pagination is demonstrated; owner/maintainer PRs are filtered correctly; Dependabot `403` is represented as unavailable; duplicate candidates are linked instead of counted twice.

### Phase 4 - Define resumable state

Specify how a run resumes after a user gate, process restart, or changed remote state. Use GitHub as the source of truth for reviews, issues, PRs, and checks. Add a compact checkpoint only if a real run demonstrates that remote state and the conversation are not sufficient. Keep checkpoints outside public repository content unless the maintainer explicitly chooses a committed tracker. Store no tokens or secrets.

**Exit criteria:** a resumed run re-fetches remote state, recognizes completed actions, avoids repeating a review on the same PR head, and never assumes a prior approval carries forward to another action.

### Phase 5 - Controlled execution

Expand from inventory to one approved work item at a time. Use clean or isolated worktrees where appropriate, inspect existing changes before edits, run repository-required checks, and wait for required remote CI before the next security merge. Keep `oss-pr-merge-readiness` focused on pre-merge readiness. After an authorized merge, route release and deployment follow-through to `oss-release-and-deploy`, which reads the repository's own release policy, monitors delivery, and verifies each public surface. The issue workflow should use the same post-merge handoff rather than duplicate it. Prepare public text in the repository's language and follow repository attribution rules.

**Exit criteria:** each local change has a reproducible validation report; public actions match the current request; pre-merge audit, merge, release, deployment, and public verification are reported as separate states; unrelated files remain untouched.

### Phase 6 - Add an automation runner

Choose a runner only after the manual workflow is reliable. Candidates include Codex scheduled automation, GitHub Actions, or another agent/orchestration product. The earlier request mentioned “Jev”; identify the intended product and verify its current API, skill-loading model, checkout access, and permission controls before selecting it.

Define cadence, target repositories, concurrency locking, timeout/retry limits, notification behavior, audit logs, pause controls, and least-privilege credentials. Scheduled runs should default to scan/report mode; public reviews and repository writes should be opt-in by an explicit policy. Never enable auto-merge or releases as an incidental part of scheduling.

**Exit criteria:** a dry-run schedule can start, report, pause, and resume without duplicate comments or overlapping work. Authorization and audit records are inspectable.

### Phase 7 - Pilot and generalize

Pilot on one repository with a small backlog, then a second repository with a different language/toolchain. Compare routing accuracy, skipped work, validation time, permission failures, and user interventions. Move only cross-repository guidance into the personal skills; keep repository-specific build/release policy in each repository's own instructions.

**Exit criteria:** the same high-level request works across both projects, while each project still runs its own required checks and respects its own support matrix and release policy.

## Success measures

- Every eligible open human PR, actionable issue, and visible Dependabot alert is accounted for, or its access gap is explicit.
- Repository-owner, member, and collaborator PRs are excluded from the external-human lane.
- The same PR head does not receive duplicate review actions.
- Product need, technical correctness, cross-language/tool consistency, repository checks, release readiness, and approval authority are reported separately.
- Security work is verified sequentially; high-risk findings are not hidden behind a routine queue.
- A `403`, failed API request, partial page set, missing skill, or unavailable runner never becomes a claim that no work exists.
- No merge, release, issue closure, alert dismissal, or contributor-branch push occurs without the required explicit authorization.
- Scheduled runs can be paused and leave an auditable summary of what they saw and did.

## Decisions to make before unattended operation

- Which repositories are in scope, and are they all public?
- What cadence and quiet-hour/notification behavior should the runner use?
- Which runner does “Jev” refer to, and can it load local skills and use the required GitHub permissions?
- Should scheduled execution remain scan-only, or may it publish `COMMENT`/`REQUEST_CHANGES` after its checks?
- Where should resumable checkpoints live if remote GitHub state is insufficient?

These decisions do not block the current interactive workflow. They do block unattended repository writes or a claim that the system is continuously monitoring repositories.

## Reference sources

- [Agent Skills specification](https://agentskills.io/specification) for skill structure, references, and progressive disclosure.
- [GitHub pull request REST API](https://docs.github.com/en/rest/pulls/pulls), [issue REST API](https://docs.github.com/en/rest/issues/issues), and [Dependabot alerts REST API](https://docs.github.com/en/rest/dependabot/alerts) for repository inventory and access requirements. Verify current documentation and permissions when implementing an adapter.
