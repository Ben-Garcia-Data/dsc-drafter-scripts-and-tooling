# Connecting an AI client to DSC Drafter (MCP setup)

This guide is written for **you or your AI assistant**. If you asked an AI to "set up
the DSC Drafter MCP server", it can follow the steps below as written.

DSC Drafter runs an MCP (Model Context Protocol) server inside the app. It is on by
default (File > Preferences > AI / Automation (MCP)), only listens on 127.0.0.1, and
only runs while DSC Drafter is open. Once connected, the AI gets these tools:
`run_python` (the full `dsc` scripting API), `screenshot` and `document_summary`,
plus the scripting documentation as resources.

## Step 1 - find the relay

AI clients connect through a small relay program that is installed next to the app:

```
C:\Users\<you>\AppData\Local\Programs\DSC Drafter\dsc_mcp_stdio.exe
```

`<you>` is the Windows user name. If DSC Drafter was installed somewhere else, the
exact path is shown in File > Preferences > AI / Automation (MCP) under
*Stdio command*, with a Copy button.

The relay takes **no arguments** and needs **no token or port**: it finds the running
app by itself, so the setup never has to change when DSC Drafter restarts.

## Step 2 - add it to your AI client

Use the full path from Step 1 everywhere below. Environment variables such as
`%LOCALAPPDATA%` are not expanded inside config files.

### Claude Desktop (the Claude app)

**Do not use "Add custom connector".** That dialog asks for a name and a *remote* MCP
server URL. Custom connectors are reached from Anthropic's servers over the internet,
so the dialog only accepts public `https://` URLs. DSC Drafter's server only listens
on this PC (`http://127.0.0.1:7333/mcp`), so the dialog rejects it, and a connector
would have no way to send its token anyway. Do not work around this by exposing the
server to the internet (for example with a tunnel). That would put full control of
the app and its Python runtime on the internet, guarded only by the token. Use the config file instead:

1. In Claude Desktop open **Settings > Developer > Edit Config**. This opens
   `claude_desktop_config.json` (normally `%APPDATA%\Claude\claude_desktop_config.json`;
   the Microsoft Store version keeps it under
   `%LOCALAPPDATA%\Packages\Claude_*\LocalCache\Roaming\Claude\`).
2. Add a `dsc` entry under `mcpServers`. In JSON every backslash must be doubled:

   ```json
   {
     "mcpServers": {
       "dsc": {
         "command": "C:\\Users\\<you>\\AppData\\Local\\Programs\\DSC Drafter\\dsc_mcp_stdio.exe"
       }
     }
   }
   ```

   If the file already has content, keep it: add `"dsc": {...}` inside the existing
   `mcpServers` object (create that object if it is missing). Do not add a second
   `mcpServers` block, and keep the file valid JSON.
3. **Fully quit** Claude Desktop (right-click its tray icon > Quit; closing the
   window is not enough) and start it again.

### Claude Code

```
claude mcp add --scope user dsc -- "C:\Users\<you>\AppData\Local\Programs\DSC Drafter\dsc_mcp_stdio.exe"
```

`--scope user` makes it available in every project. Start a new Claude Code session
afterwards; `/mcp` lists `dsc` as connected while DSC Drafter is open.

### Codex CLI

Add to `%USERPROFILE%\.codex\config.toml`:

```toml
[mcp_servers.dsc]
command = 'C:\Users\<you>\AppData\Local\Programs\DSC Drafter\dsc_mcp_stdio.exe'
```

### Cursor, VS Code and other clients

Any client that can launch a local ("stdio") MCP server works: give it the relay path
as the command, with no arguments. Cursor uses the same `mcpServers` JSON as Claude
Desktop (in `%USERPROFILE%\.cursor\mcp.json`). VS Code uses `"servers"` instead, with
`"type": "stdio"` next to `"command"`.

## Step 3 - check it works

1. Open DSC Drafter.
2. In the AI client, ask: "Use the dsc tools to give me a summary of the open drawing."
   The AI should call `document_summary` and describe the drawing.

## Alternative: HTTP (not recommended)

Clients running **on this PC** that only speak MCP streamable HTTP can connect directly
to the URL shown in Preferences (normally `http://127.0.0.1:7333/mcp`), sending the Token as `Authorization: Bearer <token>`. The token changes
every time DSC Drafter starts, so the client must be updated each time. Use the relay
whenever the client supports it.

## Troubleshooting

- **"The DSC Drafter MCP server is not running"**: the setup is correct; DSC Drafter
  is closed, or the MCP box in Preferences is unticked. Open the app (tick the box and
  click OK if needed) and retry. The relay always answers, even with the app closed,
  so the client never hangs.
- **The client says the server "failed to start" or "disconnected" straight away**:
  the relay path is wrong. This is not caused by DSC Drafter being closed, because the
  relay starts fine without the app. Check that the file named in the config exists,
  and copy the exact path from Preferences > *Stdio command*.
- **The `dsc` tools don't appear at all**: the client didn't load its config. Check
  the path points at an existing `dsc_mcp_stdio.exe`, the JSON is valid (doubled
  backslashes, no trailing commas), and the client was fully restarted.
- **"URL must start with https://" in Claude's custom connector dialog**: expected,
  see Claude Desktop above. Close the dialog and use the config file.
