---
name: devto-publish-expert
description: Research, write, optimize, validate, and publish specialist technical articles for DEV Community with exactly four relevant tags and a draft-first safety workflow. Use when creating, rewriting, reviewing, scheduling, or publishing DEV.to tutorials, project launches, engineering explainers, case studies, or opinionated developer posts, including through a DEV/Forem MCP server or API.
---

# DEV.to Publish Expert

Create technically credible articles that earn attention through usefulness, specificity, and a strong reader promise. Never fabricate results, popularity, benchmarks, quotes, or personal experience.

## Workflow

1. Establish the article goal, intended reader, language, source material, and desired action.
2. Inspect the author's existing DEV.to posts when account tools are available. Avoid duplicate angles and reuse the author's authentic voice without copying passages.
3. Research every unstable or non-obvious technical claim with current primary sources. Preserve source links near the relevant claims.
4. Choose the format and outline using [references/editorial-playbook.md](references/editorial-playbook.md).
5. Draft the article in Markdown. Lead with the reader's problem and concrete outcome; reveal the implementation progressively.
6. Select exactly four distinct, valid DEV.to tags. Use the tag strategy in the editorial playbook; never add an irrelevant popular tag for reach.
7. Perform the editorial and technical review below.
8. If a file artifact is useful, add DEV-compatible front matter and run `python scripts/validate_article.py ARTICLE.md`.
9. When DEV tools are available, follow [references/devto-publishing.md](references/devto-publishing.md). Create a draft by default.
10. Return the draft ID, its actual status, validation results, and the dashboard location. Never describe a temporary draft slug as a working preview URL.

## Required article qualities

- Deliver the promised outcome with runnable or clearly labeled illustrative examples.
- Explain why decisions were made, not only which commands to copy.
- State prerequisites, versions, assumptions, limits, risks, and tradeoffs where relevant.
- Use a concrete title that creates curiosity without hiding the subject.
- Make the first three paragraphs useful without requiring prior project context.
- Prefer short paragraphs, descriptive headings, lists only when they improve scanning, and fenced code with language identifiers.
- Include a reproducible verification step or an honest way to evaluate the result.
- End with a specific takeaway, next action, or focused discussion question.
- Link primary documentation and original projects rather than search results or aggregators.
- Keep promotion subordinate to the tutorial or insight.

## Four-tag contract

Require exactly four tags:

1. one primary subject tag;
2. one technology or ecosystem tag;
3. one article-format or audience tag when genuinely applicable;
4. one narrower discovery tag tied to the actual content.

Normalize tags to lowercase DEV-compatible slugs. Reject duplicates and irrelevant tags. Confirm current tag availability through DEV search or the connected tool when possible.

## Editorial review

Before creating a draft, verify:

- The title and opening accurately match the article.
- Every factual claim is supported by the implementation, supplied evidence, or a cited primary source.
- Commands and code use consistent names and contain no secrets.
- The reader can distinguish tested code from pseudocode.
- The article does not promise virality, rankings, reactions, or outcomes.
- The conclusion adds a decision, lesson, or next step instead of repeating the introduction.
- Exactly four tags are present.

## Publication boundary

Treat draft creation as reversible and public publication as an external side effect.

- Default to `published: false`.
- Create or update a public article only when the user explicitly requests publication in the current conversation.
- Before publishing, show the final title, description, four tags, canonical URL if any, and whether the article was validated.
- Never infer publication approval from approval to write, revise, preview, or save a draft.
- If the available integration cannot retrieve authenticated drafts, direct the user to `https://dev.to/dashboard` and report that limitation.

## Output contract

Provide:

- final title;
- one-sentence reader promise;
- short description;
- exactly four tags;
- complete Markdown;
- primary sources used;
- validation status;
- DEV.to status and article ID when a tool was called.

Do not claim that quality guarantees virality. Describe the article as optimized for clarity, credibility, discoverability, and discussion potential.
