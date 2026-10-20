# Gates

**Hard stops** wait for explicit user approval. **Automatic steps** run as
soon as GATE-PLAN is approved. A one-off “stop here” in that message still
wins.

| Gate | Kind | Agent must not proceed without |
|------|------|--------------------------------|
| GATE-VALIDATE | light; skip if obvious | Implementing when the issue is stale or a duplicate |
| GATE-PLAN | **hard stop** | Coding, the issue comment, or the PR |
| GATE-ISSUE-COMMENT | **automatic** after GATE-PLAN | - post the comment in the repository's required language (English by default); do not ask, do not offer to skip |
| GATE-COMMIT | **automatic** after GATE-PLAN | - commit, push, and open the PR on this repo; do not ask |
| GATE-MERGE | **hard stop** (recommendation only until asked) | `gh pr merge` |
| GATE-RELEASE | **hard stop** | Tags, publish, draft release publish |

Approving GATE-PLAN means: post the issue comment, implement, commit, push,
and open the PR. Merge and release still wait.

Stop-early examples (user words count):

- "only plan, no code"
- "stop after the PR is open"
