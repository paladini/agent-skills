# DEV.to Publishing Workflow

## Tool selection

Prefer an authenticated DEV/Forem integration over public username lookup when working with the user's own drafts. Public article endpoints may return 404 for unpublished articles.

When a connected MCP server exposes equivalent tools:

1. list the author's published articles for voice and duplication checks;
2. create the article with `published: false`;
3. retain the returned article ID;
4. direct the author to `https://dev.to/dashboard` for review;
5. publish only after explicit approval.

## Article payload

Use:

```json
{
  "article": {
    "title": "A specific title",
    "description": "A concise reader promise.",
    "body_markdown": "# ...",
    "tags": ["tag1", "tag2", "tag3", "tag4"],
    "published": false
  }
}
```

The exact wrapper and tag representation can vary between MCP tools. Follow the callable tool schema rather than assuming the raw API shape.

## Draft URL caveat

Do not present a returned `temp-slug` as a usable public or preview link. A valid draft preview may require opening the draft from the authenticated dashboard and obtaining a tokenized preview URL. Report the ID and dashboard link when the integration does not expose that URL.

## Publishing checklist

- Confirm title and description.
- Confirm exactly four tags.
- Confirm Markdown, images, and links render.
- Confirm canonical URL when cross-posting.
- Confirm code and claims were validated.
- Ask for explicit publication approval.
- Set `published: true` only after approval.
