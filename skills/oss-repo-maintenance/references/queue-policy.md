# Queue and routing policy

Read this reference after identifying the repository and before selecting work. The GitHub inventory is evidence for triage, not authorization to change remote state.

## Inventory sources

1. Resolve the canonical repository and default branch from GitHub or the configured Git remote. Read the authenticated account separately from the repository owner.
2. List every open pull request and every open issue. Paginate until complete. GitHub's [pull request API](https://docs.github.com/en/rest/pulls/pulls) and [issue API](https://docs.github.com/en/rest/issues/issues) document these inventories. The issues endpoint can also return pull requests, so filter records by their `pull_request` field when using that endpoint.
3. Check open Dependabot alerts when the GitHub connection permits it, then list open pull requests authored by Dependabot. Correlate an alert with its Dependabot PR so the same dependency problem is not handled twice.
4. Read repository contribution, security, product-direction, support, and release documentation. Use official vendor/advisory sources for version-sensitive or security claims.

GitHub's [Dependabot alerts API](https://docs.github.com/en/rest/dependabot/alerts) can return `403` when the token lacks the required repository permission or the account lacks access. A `403`, unavailable endpoint, incomplete pagination, or disconnected integration means **not verified**, not zero alerts. Use an authorized GitHub UI or CLI source if available. You may also inspect Dependabot PRs and run the repository's existing ecosystem audit command, but those do not prove that the full Dependabot alert inventory was visible. Do not rely only on a `security` label. Report any remaining gap.

## Eligibility and deduplication

- The repository owner's own PRs are never candidates for this queue. Also keep PRs with author association `OWNER`, `MEMBER`, or `COLLABORATOR` out of the external-human lane. If ownership or association is missing or ambiguous, do not act on the PR; report it for classification.
- Route `dependabot[bot]` PRs to the dependency lane. Do not treat automated dependency PRs as external human contributions. Do not silently expand the lane to unrelated bots such as Renovate.
- Do not submit the same review again if the current PR head commit already has a maintainer review that addresses it. If the head changed afterward, re-evaluate the new diff and prior conversation before deciding whether a new review is needed.
- Skip draft PRs until ready for review, but include them in the deferred count. Skip an issue already linked to an open PR, duplicate issues, and issues whose evidence shows they are closed, invalid, or outside the product scope.
- A reporter, issue label, bot recommendation, or CI status alone does not prove an issue is actionable. Check current behavior, reproducibility, existing plans, and recent repository decisions.

## Work order

### 0. Urgent security exception

Before the normal queue, identify evidence of a critical or actively exploited vulnerability affecting a supported, reachable component. Confirm the advisory, affected version/range, and repository exposure using current authoritative sources. If verified, elevate that item and explain why it preempts the normal order. Do not infer exploitation from severity alone.

### 1. External human pull requests

Process eligible, review-ready PRs that have not received a review on their current head. Use `oss-pull-request-review` for product need, fit, design consistency across related implementations, correctness, and the contributor response. Where the conclusion is to accept in principle and merge is under consideration, run `pr-release-audit` after the product-fit decision for pre-merge readiness. After an authorized merge, route delivery follow-through to `oss-release-and-deploy`; any release still needs its separate authorization, and any later release-preparation PR has its own merge gate. Preserve the contributor's branch and follow its authorization limits.

### 2. Actionable open issues

Select an open issue with a concrete, current, in-scope problem and no open PR already addressing it. Check for duplicates, existing work, and whether the user impact is demonstrated. Route it through `oss-github-issue-to-release`; that skill owns planning and implementation. Stop at its user gates and save or report its next action. Do not start another issue implementation while the current one is waiting for plan approval.

### 3. Dependabot alerts and pull requests

Process open security alerts and their associated PRs before routine dependency updates. Establish whether the vulnerable dependency is direct or transitive, runtime or development-only, reachable or otherwise material under the project architecture, and whether a patched version is compatible. Review an existing Dependabot PR against the actual current default branch and the current advisory. Use `pr-release-audit` for pre-merge readiness and the project's checks. After an authorized merge, use `oss-release-and-deploy` for delivery verification and any separately authorized release.

If an actionable alert has no Dependabot PR, prepare the smallest remediation plan. Do not dismiss the alert or create a public issue/PR unless the run explicitly authorizes it or the applicable issue workflow's gate has been approved. For dependency/security PRs, validate one fix locally and wait for its required remote checks before proceeding to another authorized merge; never batch merges.

## Authorization and stop conditions

- Read and analysis may continue across independent queue items after one item hits a tool or permission limit. Do not continue an item through a blocked gate.
- For a scan-only request, keep PR assessments private. When the user asks to review or process external PRs, `COMMENT` or `REQUEST_CHANGES` is within that requested review workflow; follow `oss-pull-request-review` and repository rules. Never submit `APPROVE` without separate explicit authorization.
- Issue creation, public issue comments, pushing commits, opening PRs, merging, closing issues, dismissing alerts, tagging, and releases each require the authorization specified by the selected skill and the user's current request. Never treat one approval as blanket permission for later actions.
- Stop the current item when its plan, merge, or release gate is pending; when product direction or security impact cannot be grounded; when local checks cannot safely run; or when repository state changed enough to invalidate the assessment. Report the evidence and smallest next decision.
- Do not retry unchanged API failures repeatedly. Use one suitable fallback; if it also fails, record the coverage gap and continue only with independent work.
