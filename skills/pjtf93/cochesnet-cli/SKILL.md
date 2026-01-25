---
name: cochesnet-cli
description: Use the cochesnet CLI to search coches.net listings and fetch listing details. Apply when a user asks for coches.net marketplace data or when you need the exact CLI commands and flags for cochesnet-cli.
compatibility: Requires cochesnet-cli installed (Node.js 18+), network access to apps.gw.coches.net.
license: MIT
metadata:
  author: pjtf93
  version: "0.1.0"
---

## Purpose
Use the cochesnet CLI to search listings and fetch ad details.

## When to use
- User asks to search coches.net listings from the terminal.
- User needs listing details for a known ad ID.
- User wants JSON output for scripting.

## Commands
### Search listings
```
cochesnet search "<query>" [--limit <n>] [--page <n>]
```

### Listing detail
```
cochesnet listing <adId>
```

### JSON output
Add `--json` to either command:
```
cochesnet search "bmw" --json
cochesnet listing 58229053 --json
```

## Configuration
Environment variables:
- `COCHESNET_BASE_URL` (default: https://apps.gw.coches.net)
- `COCHESNET_APP_VERSION` (default: 7.94.0)
- `COCHESNET_HTTP_USER_AGENT` (default: coches.net 7.94.0)
- `COCHESNET_X_USER_AGENT` (default: 3)
- `COCHESNET_TENANT` (default: coches)
- `COCHESNET_VARIANT` (optional X-Adevinta-MT-Variant header)

## Output expectations
- Search: table or JSON with id, title, price, year, km, location, url.
- Listing: table or JSON with title, price, url, seller, description.

## Examples
```
cochesnet search "bmw" --limit 5
cochesnet search "toyota" --page 2
cochesnet listing 58229053
```

## Error handling
- Non-zero exit code on failure.
- For scripting, use `--json` and check exit code.
