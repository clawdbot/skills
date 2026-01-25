---
name: idealista-cli
description: Use the idealista CLI to search Idealista listings by location (city, town, area, street) and fetch listing details. Apply when a user asks for Idealista marketplace data or needs CLI commands/flags for idealista-cli.
compatibility: Requires idealista-cli installed (Node.js 18+), network access to app.idealista.com.
license: MIT
metadata:
  author: pjtf93
  version: "0.1.0"
---

## Purpose
Search Idealista listings and fetch listing details.

## When to use
- User wants Idealista searches by city/town/area/street.
- User needs listing detail by ad ID.
- User wants JSON output for scripting.

## Commands
### Location suggestions
```
idealista locations "<query>" --operation <sale|rent|transfer> --property-type <homes|rooms|offices|garages|land>
```

### Search listings
```
idealista search "<query>" --operation <sale|rent|transfer> --property-type <homes|rooms|offices|garages|land>
```

Optional filters:
- `--page <n>`
- `--limit <n>`
- `--min-price <amount>` / `--max-price <amount>`
- `--min-size <sqm>` / `--max-size <sqm>`
- `--bedrooms <count>`
- `--order <field>` / `--sort <order>`
- `--location-id <id>` to skip lookup

### Listing detail
```
idealista listing <adId>
```

### JSON output
Add `--json` to any command:
```
idealista search "madrid" --json
idealista listing 123456789 --json
```

## Configuration
Defaults are prefilled from APK, override via env vars if needed:
- `IDEALISTA_API_KEY`
- `IDEALISTA_SIGNATURE_SECRET`
- `IDEALISTA_OAUTH_CONSUMER_KEY`
- `IDEALISTA_OAUTH_CONSUMER_SECRET`
- `IDEALISTA_DEVICE_ID`
- `IDEALISTA_APP_VERSION`
- `IDEALISTA_BASE_URL`
- `IDEALISTA_USER_AGENT`
- `IDEALISTA_DNT`

## Output expectations
- Locations: table or JSON with `locationId`, name, type.
- Search: table or JSON with id, price, rooms, size, address, location, url.
- Listing: table or JSON with price, rooms, size, address, url, description.

## Examples
```
idealista locations "madrid" --operation sale --property-type homes
idealista search "madrid" --operation rent --property-type homes --limit 20
idealista listing 123456789
```

## Error handling
- Non-zero exit code on failure.
- For scripting, use `--json` and check exit code.
