# Publishing MCP Configurations

Sanitized, reproducible MCP client examples for DEV.to, Medium, and LinkedIn publishing workflows. These files contain placeholders only. Never commit API keys, cookies, browser profiles, storage-state files, or copied client configuration containing real secrets.

## Collection

| Platform | Server | Authentication | Default publication boundary |
| --- | --- | --- | --- |
| DEV.to | [`Arindam200/devto-mcp`](https://github.com/Arindam200/devto-mcp) | `DEV_TO_API_KEY` supplied locally | Create draft with `published: false` |
| Medium | [`@playwright/mcp`](https://github.com/microsoft/playwright-mcp) | Manual login in isolated persistent browser profile | Edit the auto-saved draft; stop before Publish |
| LinkedIn | [`@playwright/mcp`](https://github.com/microsoft/playwright-mcp) | Manual login in isolated persistent browser profile | Prepare content; stop before the final Post/Publish action |

The browser configurations use Playwright MCP `0.0.69` for reproducibility. Review upstream releases and update the pin deliberately when restoring the collection.

## Restore DEV.to

1. Clone the server:

   ```powershell
   git clone https://github.com/Arindam200/devto-mcp.git C:\MCPs\devto-mcp
   ```

2. Install [`uv`](https://docs.astral.sh/uv/) and use a supported Python version. The configuration previously validated on Windows with Python `3.13.5`.
3. Ensure STDIO diagnostics are written to stderr. Any startup banner written to stdout corrupts MCP protocol traffic.
4. Copy either [`devto/codex.toml.example`](devto/codex.toml.example) or [`devto/client.json.example`](devto/client.json.example) into the appropriate client configuration.
5. Replace paths and set `DEV_TO_API_KEY` only in the local client configuration or secret manager. Use [`devto/.env.example`](devto/.env.example) only as a variable-name reference.
6. Restart the MCP client and test read-only tools before creating a draft.

For Codex, confirm registration with:

```powershell
codex mcp list
codex mcp get devto
```

## Restore Medium or LinkedIn

1. Install Node.js 18 or newer.
2. Copy the platform's TOML or JSON example into the MCP client configuration.
3. Replace `C:\PATH\TO\...\browser-profile` with an absolute directory outside this Git repository.
4. Restart the MCP client. The first browser session should be visible because headed mode is the default.
5. Log in manually. Do not place the username, password, MFA secret, cookies, or storage state in these files.
6. Ask the agent to prepare the post and stop at the publication boundary described in [publishing-guardrails.md](publishing-guardrails.md).

Each platform uses a distinct profile directory because a persistent Playwright profile can be used by only one browser process at a time and must not share authentication state unintentionally.

## Client formats

- `codex.toml.example` contains a table to merge into `~/.codex/config.toml`.
- `client.json.example` contains an `mcpServers` object for clients that accept the common JSON shape.
- Paths are deliberately invalid placeholders. Replace them locally; do not commit the resolved paths if they reveal sensitive usernames or storage locations.

## What is intentionally absent

- Real API keys or environment values.
- Passwords, MFA recovery codes, cookies, tokens, or browser storage state.
- Selectors or scripts that blindly click Publish.
- Claims that browser automation is stable across platform redesigns.
- Platform-specific scraping or anti-bot bypasses.

Medium and LinkedIn can change their interfaces and policies without notice. Browser automation must remain supervised, use the account owner's normal session, and comply with the platform's current terms.
