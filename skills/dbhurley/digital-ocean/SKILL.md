---
name: digital-ocean
description: Manage Digital Ocean droplets, domains, and infrastructure via DO API.
homepage: https://docs.digitalocean.com/reference/api/
metadata: {"clawdis":{"emoji":"🌊","requires":{"bins":["uv","curl"],"env":["DO_API_TOKEN"]},"primaryEnv":"DO_API_TOKEN"}}
---

# Digital Ocean Management

Control DO droplets, domains, and infrastructure.

## Setup

Set environment variable:
- `DO_API_TOKEN`: Your Digital Ocean API token (create at cloud.digitalocean.com/account/api/tokens)

## CLI Commands

```bash
# Account info
uv run {baseDir}/scripts/do.py account

# List all droplets
uv run {baseDir}/scripts/do.py droplets

# Get droplet details
uv run {baseDir}/scripts/do.py droplet <droplet_id>

# List domains
uv run {baseDir}/scripts/do.py domains

# List domain records
uv run {baseDir}/scripts/do.py records <domain>

# Droplet actions
uv run {baseDir}/scripts/do.py power-off <droplet_id>
uv run {baseDir}/scripts/do.py power-on <droplet_id>
uv run {baseDir}/scripts/do.py reboot <droplet_id>
```

## Direct API (curl)

### List Droplets
```bash
curl -s -H "Authorization: Bearer $DO_API_TOKEN" \
  "https://api.digitalocean.com/v2/droplets" | jq '.droplets[] | {id, name, status, ip: .networks.v4[0].ip_address}'
```

### Get Account Info
```bash
curl -s -H "Authorization: Bearer $DO_API_TOKEN" \
  "https://api.digitalocean.com/v2/account" | jq '.account'
```

### List Domains
```bash
curl -s -H "Authorization: Bearer $DO_API_TOKEN" \
  "https://api.digitalocean.com/v2/domains" | jq '.domains[].name'
```

### Create Droplet
```bash
curl -s -X POST -H "Authorization: Bearer $DO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-droplet",
    "region": "nyc1",
    "size": "s-1vcpu-1gb",
    "image": "ubuntu-22-04-x64"
  }' \
  "https://api.digitalocean.com/v2/droplets"
```

### Reboot Droplet
```bash
curl -s -X POST -H "Authorization: Bearer $DO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"reboot"}' \
  "https://api.digitalocean.com/v2/droplets/<DROPLET_ID>/actions"
```

### Add Domain
```bash
curl -s -X POST -H "Authorization: Bearer $DO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "example.com"}' \
  "https://api.digitalocean.com/v2/domains"
```

## Notes

- Always confirm before destructive actions (power-off, destroy)
- Token requires read/write scope for management actions
- API docs: https://docs.digitalocean.com/reference/api/api-reference/
