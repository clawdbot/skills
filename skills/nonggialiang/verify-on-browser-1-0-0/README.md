# Browser CDP MCP Server

A minimal MCP (Model Context Protocol) server that provides direct access to the Chrome DevTools Protocol (CDP) for maximum flexibility browser control.

## Features

- **Raw CDP Access**: Call any Chrome DevTools Protocol method directly via `cdp_send`
- **Screenshot Capture**: Take screenshots in PNG or JPEG format
- **URL Retrieval**: Get the current page URL
- **Browser Management**: Launch and close browser instances

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

The server communicates over stdio using the MCP protocol.

## Tools

### `cdp_send`
Execute any CDP method. Reference: https://chromedevtools.github.io/devtools-protocol/

**Parameters:**
- `method` (string): CDP method name (e.g., `Page.navigate`, `DOM.getDocument`, `Runtime.evaluate`)
- `params` (object, optional): Parameters for the CDP method

**Example:**
```json
{
  "method": "Page.navigate",
  "params": { "url": "https://example.com" }
}
```

### `screenshot`
Capture a screenshot of the current page.

**Parameters:**
- `format` (string, optional): `"png"` or `"jpeg"` (default: `"png"`)
- `fullPage` (boolean, optional): Capture full scrollable page (default: `false`)

### `get_url`
Returns the current page URL.

### `close_browser`
Closes the browser instance and cleans up resources.

## MCP Configuration

Add to your MCP client configuration:

```bash
claude mcp add-json browser '{
  "type": "stdio",
  "command": "node",
  "args": ["path/to/browser-tool/server.js"]
}' --scope user
```

## Skill Integration
Add the browser skill to claude:

```bash
cp .path/to/browser-tool/.claude/skills/browser.md ~/.claude/skills/browser.md
```

## Dependencies

- `@modelcontextprotocol/sdk` - MCP SDK for server implementation
- `playwright` - Browser automation
- `zod` - Schema validation

## License

MIT
