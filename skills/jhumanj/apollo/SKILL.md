---
name: apollo
description: Interact with Apollo.io REST API (people/org enrichment, search, lists).
metadata: {"clawdbot":{"emoji":"🛰️","os":["darwin","linux"]}}
---

# Apollo.io

Interact with Apollo.io via REST API.

## Config

Create `config/apollo.env` (example at `config/apollo.env.example`):

- `APOLLO_BASE_URL` (usually `https://api.apollo.io`)
- `APOLLO_API_KEY`

Scripts load this automatically.

## Commands

### Low-level helpers

- GET: `skills/apollo/scripts/apollo-get.sh "/api/v1/users"` (endpoint availability may vary)
- People search (new): `skills/apollo/scripts/apollo-people-search.sh "vp marketing" 1 5`
- POST (generic): `skills/apollo/scripts/apollo-post.sh "/api/v1/mixed_people/api_search" '{"q_keywords":"vp marketing","page":1,"per_page":5}'`

### Enrichment (common)

- Enrich website/org by domain: `skills/apollo/scripts/apollo-enrich-website.sh "apollo.io"`
- Get complete org info (bulk): `skills/apollo/scripts/apollo-orgs-bulk.sh "6136480939c707388501e6b9"`

## Notes

- Apollo authenticates via `X-Api-Key` header (these scripts send it automatically).
- Some endpoints require a **master API key** and a paid plan (Apollo returns `403` in that case).
- Rate limiting is common (e.g. 600/hour on many endpoints); handle `429` responses.
