# JustWatch Integration

## Overview

JustWatch provides streaming availability data. We use TMDB's integrated watch/providers endpoint which sources data from JustWatch.

## How It Works

1. TMDB has a partnership with JustWatch
2. When we fetch movie/TV details with `append_to_response=watch/providers`, TMDB returns JustWatch data
3. No separate JustWatch API key needed

## Watch Region

Set user's region in `services.json`:

```json
{
  "active": ["netflix", "amazon-prime"],
  "region": "DE"
}
```

Supported regions: DE, AT, CH, US, UK, FR, ES, IT, etc.

## Availability Types

| Type | Meaning |
|------|---------|
| `flatrate` | Included with subscription (what we care about most) |
| `rent` | Available to rent |
| `buy` | Available to purchase |
| `free` | Free with ads |

## Matching User Services

When checking availability:

1. Get `flatrate` providers from TMDB response
2. Compare provider names against user's `active` services
3. Mark as "available" if there's a match

## Caching

- Cache availability data for 24 hours
- Streaming rights change frequently, but not hourly
- Reduces API calls and speeds up responses

## Limitations

- TMDB data may be 1-2 days behind JustWatch
- Some regional differences may not be accurate
- New releases may take time to appear

## Alternative: Direct JustWatch API

If more detailed data is needed, JustWatch has a GraphQL API:

```
POST https://apis.justwatch.com/graphql
```

Requires:
- Custom headers
- Rate limiting (be careful)
- No official API key (scraping territory)

For most use cases, TMDB's integrated data is sufficient and more reliable.
