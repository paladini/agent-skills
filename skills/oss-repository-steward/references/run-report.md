# Sweep report

Use this format at the end of each run. Keep verified facts separate from recommendations and unavailable data.

## Repository sweep

- Repository and default branch:
- Scan time and inventory coverage:
- Eligible external PRs:
- Actionable open issues:
- Dependabot alerts and PRs:
- Unavailable sources or permission gaps:

## Processed

For each item, list its URL, type, conclusion, public/local actions actually taken, and checks actually run. Link the relevant review, issue workflow brief, PR, or audit when available.

## Deferred or skipped

For each item, list its URL and one reason: owner/maintainer PR, draft, already reviewed at current head, duplicate, open linked PR, not actionable, out of scope, stale, or blocked by a user gate. Do not imply that skipped work was completed.

## Waiting on the user

List each pending decision by the exact gate or action, the evidence needed to decide, and the effect of approving it. Keep plan, public review, merge, and release authorization separate.

## Next action

Name the single highest-priority remaining item, or state that the initial queue is exhausted. If the run stopped because of a gate or unavailable data, state that plainly rather than claiming there is no work.
