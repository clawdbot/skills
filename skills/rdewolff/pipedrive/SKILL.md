---
name: pipedrive
description: Pipedrive CRM API for managing deals, contacts (persons), organizations, activities, leads, pipelines, products, and notes. Use for sales pipeline management, deal tracking, contact/organization management, activity scheduling, lead handling, or any Pipedrive CRM tasks.
---

# Pipedrive

Sales CRM API for deals, contacts, organizations, activities, pipelines, leads, and notes.

## Setup

Get your API token from Pipedrive:
1. Go to Settings → Personal preferences → API
2. Copy your personal API token

Store in `~/.clawdbot/clawdbot.json`:
```json
{
  "skills": {
    "entries": {
      "pipedrive": {
        "apiToken": "YOUR_API_TOKEN"
      }
    }
  }
}
```

Or set env: `PIPEDRIVE_API_TOKEN=xxx`

## Quick Reference

### Deals (most important!)
```bash
{baseDir}/scripts/pipedrive.sh deals list                    # List all deals
{baseDir}/scripts/pipedrive.sh deals list --status open      # Open deals only
{baseDir}/scripts/pipedrive.sh deals search "query"          # Search deals
{baseDir}/scripts/pipedrive.sh deals show <id>               # Get deal details
{baseDir}/scripts/pipedrive.sh deals create --title "Deal" --person <id> --value 1000
{baseDir}/scripts/pipedrive.sh deals update <id> --value 2000 --stage <stage_id>
{baseDir}/scripts/pipedrive.sh deals won <id>                # Mark deal as won
{baseDir}/scripts/pipedrive.sh deals lost <id> --reason "Reason"  # Mark deal as lost
{baseDir}/scripts/pipedrive.sh deals delete <id>             # Delete deal
```

### Persons (contacts)
```bash
{baseDir}/scripts/pipedrive.sh persons list                  # List all persons
{baseDir}/scripts/pipedrive.sh persons search "query"        # Search persons
{baseDir}/scripts/pipedrive.sh persons show <id>             # Get person details
{baseDir}/scripts/pipedrive.sh persons create --name "John Doe" --email "john@example.com"
{baseDir}/scripts/pipedrive.sh persons update <id> --phone "+1234567890"
{baseDir}/scripts/pipedrive.sh persons delete <id>           # Delete person
```

### Organizations
```bash
{baseDir}/scripts/pipedrive.sh orgs list                     # List all organizations
{baseDir}/scripts/pipedrive.sh orgs search "query"           # Search organizations
{baseDir}/scripts/pipedrive.sh orgs show <id>                # Get organization details
{baseDir}/scripts/pipedrive.sh orgs create --name "Acme Corp"
{baseDir}/scripts/pipedrive.sh orgs update <id> --address "123 Main St"
{baseDir}/scripts/pipedrive.sh orgs delete <id>              # Delete organization
```

### Activities
```bash
{baseDir}/scripts/pipedrive.sh activities list               # List activities
{baseDir}/scripts/pipedrive.sh activities list --done 0      # Upcoming activities
{baseDir}/scripts/pipedrive.sh activities show <id>          # Get activity details
{baseDir}/scripts/pipedrive.sh activities create --subject "Call" --type call --deal <id>
{baseDir}/scripts/pipedrive.sh activities done <id>          # Mark activity done
```

### Pipelines & Stages
```bash
{baseDir}/scripts/pipedrive.sh pipelines list                # List all pipelines
{baseDir}/scripts/pipedrive.sh pipelines stages <pipeline_id>  # List stages in pipeline
```

### Leads
```bash
{baseDir}/scripts/pipedrive.sh leads list                    # List all leads
{baseDir}/scripts/pipedrive.sh leads show <id>               # Get lead details
{baseDir}/scripts/pipedrive.sh leads create --title "New Lead" --person <id>
{baseDir}/scripts/pipedrive.sh leads convert <id>            # Convert lead to deal
```

### Products
```bash
{baseDir}/scripts/pipedrive.sh products list                 # List all products
{baseDir}/scripts/pipedrive.sh products search "query"       # Search products
```

### Notes
```bash
{baseDir}/scripts/pipedrive.sh notes list --deal <id>        # Notes for a deal
{baseDir}/scripts/pipedrive.sh notes list --person <id>      # Notes for a person
{baseDir}/scripts/pipedrive.sh notes create --content "Note text" --deal <id>
```

## Deal Statuses

- `open` - Active deal in pipeline
- `won` - Deal closed-won
- `lost` - Deal closed-lost
- `deleted` - Deleted deal

## Activity Types

Common types: `call`, `meeting`, `task`, `deadline`, `email`, `lunch`

## Notes

- API Base: `https://api.pipedrive.com/v1`
- Auth: API token via `api_token` query param
- Rate limit: 10 req/second, 100,000/day per company
- Pagination: Use `start` (offset) and `limit` params
- Always confirm before creating/updating/deleting records

## API Reference

For detailed endpoint documentation, see [references/api.md](references/api.md).
