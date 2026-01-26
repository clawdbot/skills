---
name: mcporter
description: Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation.
homepage: https://github.com/pdxfinder/mcporter
metadata: {"clawdbot":{"emoji":"🔌","os":["darwin","linux","windows"],"requires":{"bins":["mcporter"]},"install":[{"id":"brew","kind":"brew","formula":"pdxfinder/tap/mcporter","bins":["mcporter"],"label":"Install mcporter (brew)"}]}}

# mcporter

Use `mcporter` to manage MCP (Model Context Protocol) servers and tools.

## Requirements
- `mcporter` CLI installed (via Homebrew: `brew install pdxfinder/tap/mcporter`)
- MCP server configuration in `~/.config/mcporter/`

## Common Commands

### List Configured Servers
```bash
mcporter list
```

### Authentication
```bash
mcporter auth --help
```

### Call MCP Tools
```bash
mcporter call <server-name> <tool-name> [arguments...]
```

### Generate CLI/Types
```bash
mcporter generate cli <server-name>
mcporter generate types <server-name>
```

### Config Management
```bash
mcporter config --help
```

## Notes
- mcporter supports both HTTP and stdio MCP servers
- Ad-hoc server creation is supported
- CLI generation creates typed wrappers for MCP tools
- Use `exec` tool to run mcporter commands
