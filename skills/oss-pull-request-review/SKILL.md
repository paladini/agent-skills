---
name: oss-pull-request-review
description: Review an external open-source contributor pull request for demonstrated need, product fit, technical correctness, and consistency across related languages, tools, and versions. Use when asked to review, assess, or decide whether to accept a community PR; do not use for routine reviews of your own implementation PRs or release-only audits.
---

# OSS Pull Request Review

Assess the contribution as a product and maintenance decision as well as a code change. Give the contributor a fair, evidence-based review and preserve the maintainer's control over approval and merge.

## Workflow

1. **Establish repository context.** Confirm the base repository, target branch, PR head, changed files, current checks, and any linked issues. Read applicable `AGENTS.md`, contribution guidance, product goals or roadmap, support matrix, architecture notes, and release policy. Search existing issues, discussions, and recent decisions for prior context. Follow repository-specific review skills and required checks when present.

2. **Assess the need and product fit.** Identify the user problem the change claims to solve, who experiences it, and evidence that the problem exists. Check whether current product behavior or documented plans already address it. Judge whether the proposed behavior fits the product's stated direction and whether its ongoing support cost is justified. The absence of an issue is not by itself evidence that a contribution is unnecessary. If direction or user need is unclear, state what is documented, what is inferred, and the assumption that drives your recommendation.

3. **Check consistency at the right scope.** Identify directly related implementations, adapters, languages, tools, and supported versions from repository documentation and code. Compare relevant behavior, public interfaces, configuration, defaults, compatibility, tests, and documentation. Expand the comparison when the change affects a shared contract, global scoring, support policy, or compatibility claim. Do not demand identical behavior from ecosystems with different capabilities; call out intentional differences and their rationale. For version-sensitive external behavior, consult current official vendor documentation when browsing is available and cite it.

4. **Review implementation quality.** Inspect the full diff and relevant surrounding code. Evaluate correctness, security, regressions, edge cases, maintainability, and compatibility. Run the repository's required and targeted checks when permitted and feasible; report what actually ran and any failures. Do not claim checks passed based only on PR metadata. Give actionable findings first, with severity and precise file or line references. Avoid style-only comments unless the repository requires them or they obscure a real issue.

5. **Use the complementary release audit only after product fit.** This skill owns the OSS contribution decision: demonstrated need, product direction, ecosystem consistency, technical review, and contributor-facing feedback. If the conclusion is to accept in principle and the user is considering merge, load and apply `pr-release-audit` when available for its distinct merge and release gates: required changesets or changelogs, explicit contributor credit, documentation and site parity, and release or deployment verification. Reuse relevant evidence already gathered; do not repeat findings. If the proposal is declined or deferred on product-fit grounds, skip the release audit unless the user explicitly requests one.

   Skills do not have a universal dependency installer. Do not download or install `pr-release-audit` automatically. If it is unavailable, continue this review using the repository's own contribution and release guidance; mention the missing companion only when it leaves a material merge or release gate unverified. Its absence does not prevent the need and product-fit review.

6. **Keep issue tracking explicit.** Search for an existing issue that tracks the need or blocker. When a concrete product or correctness gap needs tracking and none exists, create a focused issue as part of the requested review. If the proposed issue scope is ambiguous, draft it and ask before creation. Link the issue to the PR through GitHub's Development sidebar or an available equivalent, then verify that the issue and PR show the relationship. A textual `Related to #N` reference alone is not proof of a formal Development link. Use a closing keyword such as `Closes #N` only when merging this PR should close the issue; otherwise use a non-closing manual link. Do not edit a contributor's PR description to add a keyword without authorization. Follow [GitHub's issue and PR linking guidance](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue). If permissions or tooling prevent linking, say so plainly and do not report the issue as linked.

7. **Choose and communicate the review outcome.** Recommend one of: accept in principle, request specific changes, or decline/defer with the product reason. When asked to review a live PR, submit `REQUEST_CHANGES` for actionable blockers and `COMMENT` for non-blocking feedback or a product discussion unless the user requested private analysis or a draft. Never submit `APPROVE` without separate, explicit authorization. Thank external contributors for their time and work, but do not frame a repository maintainer as an external contributor. Explain product-fit decisions with concrete evidence and alternatives where useful. Write public repository feedback in the repository's required language.

## Authorization boundaries

- Never submit `APPROVE` or merge a PR without separate, explicit user authorization, even when the review is positive.
- Do not push changes to a contributor's branch or alter the PR unless the user explicitly requests that work.
- Treat issue creation as a public action. For a requested PR review, create a focused issue when a concrete gap needs tracking and no relevant issue exists; if the scope or ownership is ambiguous, draft it and ask first.
- If you cannot inspect the base branch, repository direction, or relevant ecosystem implementations, state the limitation and narrow the conclusion instead of guessing.

## Review report

Present the conclusion in this order:

1. Product need and fit, including evidence and assumptions.
2. Blocking and non-blocking code findings, with severity and locations.
3. Cross-language, tool, or version consistency findings within the relevant scope.
4. Checks run and their results.
5. Existing or newly created issue, its verified PR link, and the proposed GitHub review action.

Lead with actionable findings when any exist. If none exist, say so and separate a positive technical assessment from the product recommendation and from approval authority.

## Example requests

- "Review this community PR and tell me whether this feature belongs in the product."
- "Compare this contributor's change with our other language implementations before I decide."
- "Check whether this PR needs an issue and make sure the relationship is visible on GitHub."
