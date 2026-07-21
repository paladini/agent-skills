# Publishing Guardrails

Apply these rules whenever an MCP server can write to a professional publishing platform.

## Default behavior

1. Research and draft without external writes when possible.
2. Validate links, claims, formatting, mentions, tags, and media.
3. Save a platform draft when the platform supports it.
4. Stop before the final public Publish, Post, or Schedule action.
5. Show the final title/body, destination account, audience, canonical URL, tags or hashtags, and scheduled time.
6. Perform the final action only after explicit approval in the current conversation.
7. Return the resulting public URL and verify it while authenticated and, when possible, logged out.

Approval to write, edit, preview, open an editor, or save a draft is not approval to publish.

## Browser sessions

- Keep one persistent profile per platform.
- Store profiles outside the repository and never sync them as backups.
- Log in manually and complete MFA yourself.
- Do not ask the agent to read, display, or export cookies or local storage.
- Keep the browser headed for publication workflows.
- Close other processes using the same profile before starting the MCP server.
- Re-authenticate normally when a session expires; do not automate anti-bot or account-recovery flows.

## Platform behavior

### DEV.to

- Prefer the authenticated API integration.
- Set `published: false` for draft creation.
- Do not treat a temporary slug as a working preview URL.
- Review drafts from `https://dev.to/dashboard`.

### Medium

- Open the official editor and allow it to save the draft.
- Confirm title, subtitle, canonical URL, topics, image attribution, and paywall/publication destination.
- Stop before the final Publish action and its confirmation dialog.

### LinkedIn

- Distinguish a short post, newsletter, and article before editing.
- Confirm the intended personal profile or organization page.
- Confirm mentions, hashtags, link preview, media, audience, and schedule.
- If the selected format has no durable draft, stop with the editor populated and ask the user to review it immediately.
- Stop before the final Post, Publish, or Schedule action.
