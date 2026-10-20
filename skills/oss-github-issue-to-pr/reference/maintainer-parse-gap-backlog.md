# Maintainer parse-gap backlog (optional schema and parsing workflow)

Use when a maintainer-authored issue is a **pre-written implementation checklist**
for schema-driven parsing, rather than a community bug report. Treat this as
optional guidance: repository conventions and the issue's scope take precedence.

## Signals

- Issue body lists schema elements, target types, fixture requirements, and
  explicit out-of-scope block.
- A linked umbrella issue points to scoped child issues.
- No external reporter credit needed (maintainer-authored backlog).

## Playbook id

Set **`maintainer-parse-gap`** in the brief (extends `community-bug` routing).

## Branch and release rhythm

1. Start from the repository's current target branch and follow its branch convention.
2. Keep one checklist issue narrowly scoped to one PR unless repository policy says otherwise.
3. Assess API and version impact under the repository's release policy; do not assume a package manager or release channel.
4. Update changelog, package metadata, or migration guidance when the repository requires it.
5. Write the PR in the repository's required language (English by default). Use a closing keyword only when the PR fully resolves the issue.
6. After CI passes, merge only with **GATE-MERGE**; release only with **GATE-RELEASE**.

## Implementation checklist (agent)

- [ ] Read issue scope **in/out**; do not implement sibling backlog items.
- [ ] Use synthetic fixtures; never commit real personal or customer data.
- [ ] Add parser and serialization round-trip coverage where applicable.
- [ ] Update relevant schema and field coverage documentation.
- [ ] Export new public types from the package entry point if the repository exposes them.
- [ ] Run repository-required verification from its contribution guidance.

## Additive TypeScript API

When adding required fields to an existing public interface, document the
compatibility impact and how callers should populate the new field. Follow the
repository's release-note conventions.

## Issue comment

After **GATE-PLAN**, acknowledge the gap in the repository's required language,
confirm the schema path, explain which values will receive typed support and
which remain in generic/raw storage, and point to the planned PR.

## Gates

Same as the default pipeline. Maintainer velocity does **not** skip GATE-MERGE or
GATE-RELEASE unless the user explicitly asks to merge/publish in that turn.
