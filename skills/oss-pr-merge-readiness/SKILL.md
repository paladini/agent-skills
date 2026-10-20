---
name: oss-pr-merge-readiness
description: Audit pre-merge readiness for a change whose need and scope have been accepted or assessed. Check correctness, tests, architecture, security, vendor compatibility, repository docs and websites, changesets, release notes, and contributor attribution. Use before merge, not for initial OSS product-fit triage or post-merge publication.
---

# PR Merge Readiness Audit

Perform an evidence-backed audit of merge readiness. Treat repository
instructions, current branch state, PR metadata, vendor contracts, CI,
generated site, and release metadata as separate evidence surfaces. This skill
ends at the merge decision; post-merge release and deployment follow-through
belongs to `oss-release-and-deploy` when available.

This audit assumes that the change's need and intended scope have been
accepted or assessed. It does not decide whether an external contribution
belongs in the product. If that decision is still open, use
[`oss-pull-request-review`](../oss-pull-request-review/SKILL.md) first when
available, then return here only if the contribution remains a candidate for
merge. Do not repeat product-fit analysis or technical findings that the first
review already established; focus on unresolved merge and release gates.

## Authority and safety

- Read `AGENTS.md`, contributor guidance, release guidance, and relevant local
  rules before changing files.
- Preserve unrelated worktree changes. Inspect status before and after edits.
- Review and diagnostics are read-only by default. Implement requested fixes,
  documentation, or pre-merge release metadata when they are in scope.
- Never merge, tag, publish packages, create a GitHub release, close issues, or
  send external messages unless the user explicitly authorizes that action.
- Do not claim that a change is released, deployed, public, or complete until
  the corresponding public state has been independently verified.

## 1. Establish the change boundary

1. Identify the repository, PR number, base and head commits, author, linked
   issue, labels, changed files, and current review/check status.
2. Compare the PR with its actual base, not with a stale local branch.
3. Classify every changed file as implementation, test, configuration, docs,
   generated output, release metadata, or unrelated noise.
4. Record the initial worktree state and do not overwrite unrelated changes.

## 2. Review implementation and structure

Check behavior before style:

- correctness, error handling, edge cases, and backward compatibility;
- public API and data-shape contracts, including sync/async behavior;
- path traversal, symlinks, generated files, platform differences, and
  incomplete or unreadable inputs when relevant;
- security, performance, determinism, and dependency/supply-chain impact;
- whether the design adds the smallest material change or creates a new
  structural coupling;
- tests for the changed behavior, regression cases, and negative cases.

Reproduce important claims with the project commands. Do not treat a green
lint job as proof that behavior, documentation, or release metadata is right.

## 3. Verify the mentioned software against current official contracts

When the change refers to a tool, framework, platform, or file path:

1. Identify the exact product and, when available, the supported version range.
2. Consult current official documentation first. For technical claims, prefer
   official docs and upstream source over blog posts or search snippets.
3. Check the documentation's last-updated/version context and verify unstable
   facts live rather than relying on memory.
4. Cross-check important paths against upstream implementation or examples.
5. Distinguish generated/runtime state from user-authored, version-controlled
   configuration.
6. Build a mapping of `upstream path or contract -> repository behavior ->
   consequence`. Flag paths that are merely conventional, deprecated, or
   undocumented.
7. Check whether the implementation is compatible with the repository's
   stated version matrix. Do not silently update the project's supported
   version policy.

If a directory is ignored, verify that it cannot contain required user config
that the scanner or product is expected to understand. Document the boundary
explicitly when generated state is intentionally excluded.

## 4. Update documentation and the site when support changes

If the PR makes a tool or workflow supported, update every relevant surface in
the same change boundary:

- README/support matrix and usage guidance;
- canonical guide page, navigation, examples, and limitations;
- all maintained locales with semantic parity, not just translated headings;
- generated metadata, sitemap, or structured data when the site uses them;
- links and anchors, including links to the tool's current official docs.

State precisely what “supported” means. Separate environment/filesystem
compatibility from detection, scoring, feature support, and runtime guarantees.
Run the repository's documentation build and link checks before merge. If the
current public site is relevant evidence, inspect it, but verify a deployment
caused by this change after merge with `oss-release-and-deploy`.

## 5. Pre-merge release metadata and contributor credit are mandatory gates

Do not rely on commit metadata alone. `Co-authored-by` is useful Git history,
but it does not guarantee that a changeset, changelog, or GitHub release note
will credit the contributor.

Before recommending merge:

1. Identify the PR author and every real contributor from PR metadata, commits,
   review history, linked issues, and explicit user-provided attribution.
2. Never invent a name or handle. Preserve the exact public GitHub handle when
   available; ask when attribution is ambiguous.
3. Ensure the source release artifact (changeset, changelog entry, or release
   note) contains an explicit, human-readable credit, such as:
   `Thanks to @handle for contributing this fix.`
4. Keep the user-facing summary useful and consistent with the project's
   documented release-note language and format.
5. For multiple contributors, credit each person whose contribution materially
   belongs in the release. Do not credit the reviewer or merge author as the
   contributor unless they actually contributed. Follow repository guidance
   when the repository owner or maintainer is also the reporter or author.
6. Verify the source release artifact and preview rendered/generated notes
   when the repository provides a local preview. Public release notes,
   registries, tags, marketplace listings, and deployed sites are verified
   after merge by `oss-release-and-deploy`.
7. If a PR is already merged and its pending release artifact lacks credit,
   report the gap and route it to `oss-release-and-deploy`; do not change
   published history or prepare a follow-up change from this pre-merge audit.

## 6. Validate proportionally

Run the project's canonical checks and any checks implied by the diff. Typical
gates include:

- unit/integration tests and type checks;
- lint and formatting;
- self-audit or sample/fixture checks;
- package/build/consumer smoke tests;
- documentation build and link validation;
- benchmark before and after scanner hot-path changes;
- CI on the supported operating systems and runtime versions;
- release preparation and version-surface checks required before merge.

Post-merge publication and deployment checks are outside this audit. Route
them to `oss-release-and-deploy` after the applicable release authorization.

Report warnings separately from failures, including pre-existing warnings and
platform-specific limitations.

## Required report

Return a concise but complete report with:

1. merge-readiness recommendation: ready, ready with follow-up, not ready, or blocked; this is an assessment, not authorization to submit an `APPROVE` review;
2. findings ordered by severity, with file and line references when useful;
3. structural, security, performance, and compatibility assessment;
4. upstream documentation evidence and path mapping;
5. documentation/site surfaces changed or still missing;
6. tests and checks run, including their exact outcome;
7. release-note/changeset status and explicit contributor-credit status;
8. merge readiness and release-metadata readiness; mark publication and
   deployment as pending, not applicable, or outside this pre-merge audit;
9. remaining risks and the smallest recommended next action.

Never summarize “green CI” as “released.” Keep local, merged, deployed, and
publicly verified states distinct.
