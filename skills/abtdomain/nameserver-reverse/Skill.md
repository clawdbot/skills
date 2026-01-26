# DomainKits MCP Server

Domain intelligence tools through MCP-compatible clients.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `https://mcp.domainkits.com/mcp/nrds` | Newly Registered Domains Search |
| `https://mcp.domainkits.com/mcp/ns-reverse` | NS Reverse Lookup |

## Configuration

### Claude Desktop

Edit config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
```json
{
  "mcpServers": {
    "domainkits-nrds": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.domainkits.com/mcp/nrds",
        "--transport",
        "http-first"
      ]
    },
    "domainkits-ns-reverse": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.domainkits.com/mcp/ns-reverse",
        "--transport",
        "http-first"
      ]
    }
  }
}
```

### Cursor

Edit `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "domainkits-nrds": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.domainkits.com/mcp/nrds"]
    },
    "domainkits-ns-reverse": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.domainkits.com/mcp/ns-reverse"]
    }
  }
}
```

---
### Gemini CLI

```bash
gemini extensions install https://github.com/ABTdomain/domainkits-mcp
```


## Tools

### search_nrds

Search for newly registered domains by keyword.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| keyword | string | Yes | - | Search term (a-z, 0-9, hyphen only, max 20 chars) |
| days | integer | Yes | - | 1-7 |
| position | string | No | any | `start`, `end`, or `any` |
| tld | string | No | all | Filter by TLD (e.g., `com`, `net`, `org`) |

**Example:**
```bash
curl -X POST https://mcp.domainkits.com/mcp/nrds \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_nrds","arguments":{"keyword":"ai","days":7,"position":"start","tld":"com"}}}'
```

---

### search_ns_reverse

Look up gTLD domains hosted on a specific nameserver.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| ns | string | Yes | - | Nameserver hostname (e.g., `ns1.google.com`) |
| tld | string | No | all | Filter by TLD (e.g., `com`, `net`, `org`) |
| min_len | integer | No | - | Minimum domain prefix length |
| max_len | integer | No | - | Maximum domain prefix length |

**Example:**
```bash
curl -X POST https://mcp.domainkits.com/mcp/ns-reverse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_ns_reverse","arguments":{"ns":"ns1.google.com","tld":"com","min_len":4,"max_len":8}}}'
```

---

## Limits

- 10 requests per minute per IP
- 5 domains per response
- NRDS data may have 24-48 hour delay

## Full Access

For complete results with advanced filters and export:
- **NRDS**: [domainkits.com/search/new](https://domainkits.com/search/new)
- **NS Reverse**: [domainkits.com/tools/ns-reverse](https://domainkits.com/tools/ns-reverse)

## About

[DomainKits](https://domainkits.com) - Domain intelligence tools for investors, brand managers, and researchers.

## Privacy

- IP addresses anonymized
- Search queries anonymized
- Logs retained 7 days
- No personal data collected

## License

MIT