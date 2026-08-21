---
name: harness-eval
description: "Evaluate a repo agent harness (AGENTS.md, rules, skills, skill refs) for broken paths/commands, redundant instructions, and usefulness using a stack-agnostic dual-judge protocol with planted traps. HIGH PRIORITY questionnaires at top: Q1 optional docs, Q2 B/C budget before Track A (certainty/tokens). A always runs after Q2; B/C opt-in. ADRs/RFCs excluded from T2. Mixed apply uses 11-mixed-apply.md (KEEP/CUT). Use when the user says harness eval, harness-eval, harness debug, audit AGENTS.md, audit skills/rules, instruction audit, redundancy of agent instructions, usefulness of skills, Ship/Review/Hold/Slim/Keep-core for harness, or wants Track A/B/C harness evaluation. Do NOT use for harness setup or init, feature spec-driven work (tlc-spec-driven), or applying Ship/Slim trims unless the user explicitly asks after the report."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 1.8.3
---

# Harness Eval

Run a full, stack-agnostic harness evaluation and stop at reports. Do not auto-edit AGENTS.md or skills unless the user explicitly asks after reviewing Ship/Slim.

## Step 0 — User briefing (HIGH PRIORITY)

**Speak this in the user's language before inventory and before Q1/Q2.** Do not paste `PROTOCOL.md`. If the user looks lost after Q2 or after the report, repeat this briefing — do not dump jargon tables first. Paraphrase [GLOSSARY.md](references/GLOSSARY.md) **Say this first**.

**What:** this audits *agent instructions* (`AGENTS.md`, rules, skills) — not application code, and not `harness-score` (or similar) maturity-point scans.

**What happens:** reports land under `.harness-eval/runs/<id>/`. **Nothing in the harness is edited** unless the user later asks to apply.

**Three tracks (user chooses B/C after a short inventory):**

- **A — Correctness** (always runs, ~0 tokens): does this cited path or command exist?
- **B — Redundancy** (optional, 2 judges × every claim): would an agent rediscover this *sentence* cheaply from the repo? Spoken: Ship = **safe to trim**, Review = **keep**, Hold = **undecided**.
- **C — Usefulness** (optional, most expensive): if this *file* disappeared, would agent behavior change, or is it theory/demo?

**Ship (B) is not Slim (C).** Obvious ≠ useless.

Humans hear this section and Step 11. `PROTOCOL.md` is the operator spec.

## User questionnaires (HIGH PRIORITY)

**Stop and ask before continuing.** Do not skip these gates. Do not silently include optional docs or spawn B/C judges.

Order: **Step 0 briefing → inventory → Q1 (if needed) → Q2 → Track A** (A always runs) → B/C only if approved.

### Q1 — Optional project docs (after inventory)

When `optional-docs-candidates.md` lists optional types, ask before Q2 / Track A. **Spoken prompt** (user's language; keep type ids for the reply):

```markdown
The audit always includes agent files (rules and skills).

I found cited *project* docs that are not agent instructions (guides, workflows, package files, …).
Include any of those in this run?

Reply with: `none` (default), type ids from the list below, and/or specific paths.
```

Then show the type/path table from `optional-docs-candidates.md` as an appendix. Do **not** lead with T2 / ADR / “decision-record trees”. (Those stay excluded in the scripts; you do not need to teach that unless asked.)

Operator fallback if you must be exact:

```markdown
Always in scope: skill-tree files (`.agents/skills`, `.cursor/skills`, `.claude/skills`).
Always excluded: ADRs / RFCs / decision-record trees.
Optional (default: omit): see `optional-docs-candidates.md`.
```

Re-run inventory with `--include-doc-type` / `--include-doc` only after the user answers. If no optional types, skip Q1.

### Q2 — Tracks B and C (before Track A — budget)

Ask **before** Track A so the user sets spend up front. Track **A always runs** next (deterministic, ~0 model tokens). B/C run only if approved.

Fill **N** from the real-claim count in `claims.md` (exclude `P00x` plants when stating N; if unsure, say the inventory claim total). Surface count ≈ T0+T1+T2 markdown after extract (or say “after surfaces_extract” if C is chosen and extract has not run).

**Spoken prompt** (user's language first, then the table):

```markdown
Track **A** always runs next: are cited paths/commands real? Script only, ~0 model tokens.

Add **B** if you want “safe to trim because this sentence is obvious from the repo”
(2 judges × N claims in this inventory — high tokens).

Add **C** if you want “does this *file* change behavior, or is it theory/demo?”
(2 judges × every whole file — highest tokens, most subjective).

Reply with one of: `A only`, `B`, `C`, or `B+C`.

Footnote: Ship (B) is not Slim (C). Obvious ≠ useless.
```

Then show the operator cost table:

```markdown
| Track | Question | Certainty | Token consumption |
|-------|----------|-----------|-------------------|
| **A — Correctness** | Cited path/command exists? | **Highest** — script only, no LLM. Prefers false negatives over false BROKEN. | **~0 model tokens** (always runs next) |
| **B — Redundancy** | Would an agent rediscover this cheaply without the harness? | **Medium** — dual LLM + plants; Ship (safe to trim) only if trap PASS and both agree. Disagree → Hold (undecided). Less model-sensitive than C. | **High** — 2 judges × every claim (~N in this inventory). Each may spot-check the repo. |
| **C — Usefulness** | Does this surface change behavior vs theory/demo/overlap? | **Lowest / most subjective** — dual LLM + plants + fan-in; **model-sensitive**. Slim/Mixed need gates; prefer second-model check before large deletes. | **Highest** — 2 judges × every surface (whole files; often dominates the run). |
```

- **`A only`:** run Track A; present `04`; stop (no B/C judges).
- **`B`:** Track A, then Steps 4–6.
- **`C`:** Track A, then Steps 7–10 (C does not need B).
- **`B+C`:** Track A, then Steps 4–11.

If the user already requested B/C/`full eval` in the triggering message, treat as approval — still show the Q2 table once so costs are visible.

## Loading this skill's files

This skill is **self-contained**. Protocol, scripts, and judge prompts live under this skill directory (the folder that contains this `SKILL.md`). Resolve `SKILL_DIR` as that directory — never assume another install path.

- Read [references/PROTOCOL.md](references/PROTOCOL.md) **completely** before the first run in a session (and again if scripts fail). Do **not** read it aloud; humans hear Step 0 and Step 11.
- Read [references/judge-prompts.md](references/judge-prompts.md) when spawning Track B or Track C judges.
- Plain-language terms: [references/GLOSSARY.md](references/GLOSSARY.md) — paraphrase **Say this first** at Step 0 and Step 11 (also embedded at the top of `04` / `07` / `10` reports).
- Claim record shape: [references/claims.schema.json](references/claims.schema.json) (for tooling; agents do not need to load it every run).
- Run scripts as `python3 "$SKILL_DIR/scripts/<name>.py" ...`.

Run **outputs** (not protocol) go to the target repo at `.harness-eval/runs/<run-id>/`.

## Critical rules

1. **Report-only by default.** Judgment ≠ remediation.
2. **README out of scope** as harness surface and as rediscovery/usefulness evidence.
3. **Stack-agnostic.** Never hard-code package managers, DBs, frameworks, or folder layouts in prompts or plants. Discover manifests that exist (JS, Python, Make/Task, Rust, Go, PHP, Ruby/Rails, Java/Gradle/Maven, plus `bin/*`).
4. **Doc scope.** T2 always includes agent skill-tree refs (`.agents/skills`, `.cursor/skills`, `.claude/skills`). **ADRs / RFCs (decision-record trees) are always excluded** from T2 surfaces. Other cited project docs are **optional** — default omit; ask via **Q1** at the top of this skill, then re-run with `--include-doc-type` / `--include-doc`.
5. **Track A always runs** after inventory (deterministic, high-precision). Prefer false negatives over false BROKEN. Placeholders (`SPEC_FOLDER`, `{x}`, `[feature]`) are never BROKEN. Never normalize paths with `str.lstrip('./')`.
6. **Tracks B and C require user approval via Q2 before Track A.** Do not spawn B/C judges until the user opts in. User may approve B only, C only, both, or A only.
7. **Track B needs dual judges + plants.** Judge2 is blind (must not read Judge1 scores or `trap-key.json`). Ship only if trap gate PASS and dual REDUNDANT with Judge2 cost ≤ 1.
8. **Track C needs dual judges + plants.** Blind Judge2 must not read `08-usefulness-j1.md` or `usefulness-trap-key.json`. Slim only if trap PASS, dual SLIM/ROUTING-ONLY, **and fan-in PASS** (no other harness surface hard-loads the path as SoT — merge enforces this on the full skill tree, not just `--seed`). **Usefulness is model-sensitive** — record `model: <id>` in both score files; prefer same model within a run; re-judge on a second model before large Slim deletes.
9. **KEEP / KEEP-CORE plants must not be verbatim copies** of claims/surfaces already in the deck.
10. **Subagents:** use an allowlisted non-fast model (prefer the same family as the parent when policy allows). Do not use `*-fast` models.
11. **Do not equate tracks.** Track B Ship ≠ Track C Slim. Rediscoverable ≠ useless; useful ≠ non-redundant.
12. **Slim apply / fan-in.** Never stub or delete a Slim path listed under “Slim fan-in blocked” (or when `python3 "$SKILL_DIR/scripts/slim_fanin.py" --path <P>` reports citers) unless those consumers are updated in the same change.
13. **Mixed/Slim apply stays self-contained.** Cutting REPO-DEMONSTRATED / THEORY means delete or compress that bulk in the harness surface. Never replace a fenced teaching snippet (or the contract it carried) with `See app/...` / `lib/...` / `test/...` — that swaps SoT for a code-tree pointer. Judge evidence paths stay in score tables only; if the behavior-changing contract must survive, keep a short in-skill rule or snippet.
14. **Mixed apply is mechanical.** Dual MIXED alone is not enough. Merge emits `11-mixed-apply.md` with per-ID **KEEP** (from Keep-core columns) and **CUT** (from Slim columns). Apply agents must follow that file only — do not re-judge, redesign, or invent a different pattern than KEEP. Empty Keep-core/Slim cells → skip that path (Hold).

## Instructions

### Step 1: Resolve SKILL_DIR

Set `SKILL_DIR` to the directory containing this `SKILL.md`. Verify:

- `$SKILL_DIR/references/PROTOCOL.md`
- `$SKILL_DIR/scripts/inventory_extract.py`
- `$SKILL_DIR/scripts/track_a_correctness.py`
- `$SKILL_DIR/scripts/merge_agreement.py`
- `$SKILL_DIR/scripts/surfaces_extract.py`
- `$SKILL_DIR/scripts/merge_usefulness.py`
- `$SKILL_DIR/scripts/slim_fanin.py`
- `$SKILL_DIR/scripts/doc_scope.py`

If missing, the skill install is broken — stop.

### Step 0: Brief the user

Deliver the [Step 0 briefing](#step-0--user-briefing-high-priority) in the user's language. Then continue to inventory. Do not start Q1/Q2 until this was said.

### Step 2: Inventory + claim deck

From the **target repo root**:

```bash
RUN_ID=$(date -u +%Y-%m-%d)-full
python3 "$SKILL_DIR/scripts/inventory_extract.py" --root . --run-id "$RUN_ID"
# Optional scope: AGENTS.md + one-hop related skills only
# python3 "$SKILL_DIR/scripts/inventory_extract.py" --root . --run-id "$RUN_ID" --seed AGENTS.md
```

Expected under `.harness-eval/runs/$RUN_ID/`: `inventory.json`, `claims.jsonl`, `claims.md`, `trap-key.json`, `optional-docs-candidates.md` (+ `.json`).

### Step 2b: Optional docs — **Q1** (see top)

Read `optional-docs-candidates.md`. If optional types exist, run **Q1** from [User questionnaires](#user-questionnaires-high-priority). Re-run inventory only after approval:

```bash
python3 "$SKILL_DIR/scripts/inventory_extract.py" --root . --run-id "$RUN_ID" \
  --include-doc-type docs   # and/or --include-doc path
```

### Step 2c: Track budget — **Q2** (see top)

Run **Q2** from [User questionnaires](#user-questionnaires-high-priority) **before** Track A. Record the answer (`A only` / `B` / `C` / `B+C`). Do not start Steps 4+ unless B and/or C were approved.

### Step 3: Track A (deterministic) — always run

```bash
python3 "$SKILL_DIR/scripts/track_a_correctness.py" --root . --run-id "$RUN_ID"
```

Expected: `04-correctness.md` (includes term definitions at top). Spot-check that `.agents/...` cites resolve (not `agents/...`).

If Q2 was `A only`, present via Step 11 (diagnosis frame, then Track A) and stop. Otherwise continue to the approved B and/or C steps; do not give the user a raw BROKEN dump as the first sentence.

### Step 4: Track B — Judge1

Read `references/judge-prompts.md` (Track B Judge1). Spawn an independent subagent with an allowlisted model. Point it at `.harness-eval/runs/$RUN_ID/claims.md`. It writes `05-redundancy-j1.md` (include `model: <id>`).

Judge1 may read `inventory.json`. Must not read `trap-key.json`.

### Step 5: Track B — Judge2 (blind)

Read `references/judge-prompts.md` (Track B Judge2). Spawn a second subagent. Writes `06-blind-scores.md`.

Forbidden for Judge2: `trap-key.json`, `05-redundancy-j1.md`, `07-agreement.md`, prior agreement reports.

Prefer Steps 4 and 5 in parallel.

### Step 6: Merge Track B agreement

```bash
python3 "$SKILL_DIR/scripts/merge_agreement.py" --run-dir .harness-eval/runs/$RUN_ID
```

Expected: `07-agreement.md` (Ship/Review/Hold + **What these words mean**). On trap FAIL: fix plants per PROTOCOL, rescore P00x, re-merge — do not Ship.

### Step 7: Track C — surface deck

```bash
python3 "$SKILL_DIR/scripts/surfaces_extract.py" --root . --run-id "$RUN_ID"
```

Expected: `surfaces.md`, `surfaces.json`, `usefulness-trap-key.json`.

### Step 8: Track C — Usefulness Judge1

Read `references/judge-prompts.md` (Usefulness Judge1). Spawn subagent with allowlisted model (record same id in header). Writes `08-usefulness-j1.md`.

Must not read `usefulness-trap-key.json`.

### Step 9: Track C — Usefulness Judge2 (blind)

Read Usefulness Judge2 prompt. Prefer **same model** as Step 8 for agreement stability. Writes `09-usefulness-j2.md`.

Forbidden: `usefulness-trap-key.json`, `08-usefulness-j1.md`, `10-usefulness-agreement.md`, and using Track B 05/06/07 to decide usefulness classes.

Prefer Steps 8 and 9 in parallel.

### Step 10: Merge Track C agreement

```bash
python3 "$SKILL_DIR/scripts/merge_usefulness.py" --run-dir .harness-eval/runs/$RUN_ID
```

Expected: `10-usefulness-agreement.md` (Slim/Keep-core/Mixed/Hold + **What these words mean**), `11-mixed-apply.md` (KEEP/CUT per Mixed ID), plus `slim-fanin.json`. On trap FAIL: do not Slim. Surfaces with `slim-fanin-blocked` are Hold — not Slim apply candidates.

### Step 11: Present results

**Fixed spoken order** — do **not** open with a BROKEN/Ship table. Paraphrase GLOSSARY **Say this first** in the user's language. File bands stay `Ship` / `Review` / `Hold`; spoken aliases: **safe to trim** / **keep** / **undecided**.

1. **Frame:** “This is a diagnosis. Nothing in `AGENTS.md` / rules / skills was changed. Reports: `.harness-eval/runs/<id>/`.”
2. **What we ran:** e.g. “A + B (you skipped C).”
3. **Track A** (`04-correctness.md`), one sentence then the list: “N cites are factually wrong (path or command missing).”
4. **Track B** if run (`07-agreement.md`), one sentence then **Ship and Hold only** (Review as a count): “Trap PASS/FAIL. Ship = both judges say safe to trim (redundant). Review = keep. Hold = they disagreed — do not trim.” If trap **FAIL**, say **ignore Ship** *before* listing any Ship rows.
5. **Track C** if run (`10-usefulness-agreement.md`): trap + fan-in + Slim / Keep-core / Mixed / Hold. Call out `11-mixed-apply.md` when Mixed count > 0. Call out Track C model ids and that Slim is model-sensitive. Call out **Slim fan-in blocked** rows.
6. **Next actions** (offer these options; do not apply unless asked): fix BROKEN / apply Ship / run Track C / stop.

Stop unless the user asks to apply Ship/Slim/Mixed. When applying:

- **Slim:** only paths in the Slim table (fan-in PASS); never stub fan-in-blocked paths without updating citers first.
- **Mixed:** open `11-mixed-apply.md` and execute KEEP/CUT per ID only (rule 12). Never re-judge from the Mixed path list alone. Never add code-tree path pointers as substitutes for cut demos (rule 11).

## Examples

### Example 1: Full harness eval

User says: "run harness eval on this repo"

Actions: Step 0 briefing (user's language) → inventory → Q1 if needed (plain spoken prompt) → Q2 (plain spoken prompt + cost table) → Track A → if approved, Steps 4–11. Parallel B judges, then C judges. Present via Step 11 template (diagnosis first, then findings).

### Example 2: Usefulness only (existing run)

User says: "run Track C usefulness on the last harness-eval run"

Actions: Steps 7–11 on that `RUN_ID` (inventory must already exist).

### Example 3: Wrong skill

User says: "setup harness" / "init harness" → harness setup (not this skill). User says: "specify feature" → tlc-spec-driven.

## Troubleshooting

### Trap gate FAIL (Track B or C)

Cause: KEEP/KEEP-CORE plants were deck duplicates, or blind judge mis-family. Solution: use skill’s fixed plant templates; rescore plants; re-merge.

### Track A false missing `.agents/...`

Cause: bad path normalization. Solution: skill script must use `normalize_cite` (strip `./` only). Re-run Track A from `$SKILL_DIR/scripts/`.

### Subagent blocked

Cause: missing/allowlisted model or `*-fast` blocked. Solution: re-spawn with an allowlisted non-fast model.

### Track C Slim looks wrong after model change

Expected: usefulness is model-sensitive. Re-run C1+C2 on a second model; intersection of Slim bands is the safe delete set.

### Mixed apply rewrote conventions / removed modules

Cause: apply agent re-judged from the Mixed path list instead of following KEEP/CUT. Solution: apply only via `11-mixed-apply.md`; if that file is missing, re-run `merge_usefulness.py`; if Keep-core/Slim cells are vague, re-score those IDs before apply.

### T2 empty / skill `references/` missing from inventory

Cause: path normalize used `lstrip("./")` and turned `.agents/…` into `agents/…`. Solution: `doc_scope.normalize_rel` must strip only a `./` prefix (same rule as Track A).

### ADRs appeared in Track C

Cause: old inventory treated all one-hop `docs/**` as T2. Solution: v1.7+ excludes decision-record trees; only user-approved optional doc types (never ADR/RFC) can enter T2.

### Slim stub broke another skill that loads that file

Cause: content OVERLAP/Slim without fan-in — older runs, or apply skipped the gate. Solution: restore the checklist body; re-merge with `merge_usefulness.py` (fan-in scans full skill trees). Confirm with `slim_fanin.py --path <P>`.

### Scripts missing

Cause: incomplete skill folder. Solution: restore `$SKILL_DIR/scripts/` and `references/`.
