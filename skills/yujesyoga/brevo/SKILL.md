---
name: brevo
version: 1.0.0
description: Brevo (formerly Sendinblue) email marketing API for managing contacts, lists, sending transactional emails, and campaigns. Use when importing contacts, sending emails, managing subscriptions, or working with email automation.
---

# Brevo Email Marketing API

Manage contacts, send emails, and automate marketing via Brevo's REST API.

## Authentication

```bash
BREVO_KEY=$(cat ~/.config/brevo/api_key)
```

All requests require header: `api-key: $BREVO_KEY`

## Base URL

```
https://api.brevo.com/v3
```

## Common Endpoints

### Contacts

| Action | Method | Endpoint |
|--------|--------|----------|
| Create contact | POST | `/contacts` |
| Get contact | GET | `/contacts/{email}` |
| Update contact | PUT | `/contacts/{email}` |
| Delete contact | DELETE | `/contacts/{email}` |
| List contacts | GET | `/contacts?limit=50&offset=0` |
| Get blacklisted | GET | `/contacts?emailBlacklisted=true` |

### Lists

| Action | Method | Endpoint |
|--------|--------|----------|
| Get all lists | GET | `/contacts/lists` |
| Create list | POST | `/contacts/lists` |
| Get list contacts | GET | `/contacts/lists/{listId}/contacts` |
| Add to list | POST | `/contacts/lists/{listId}/contacts/add` |
| Remove from list | POST | `/contacts/lists/{listId}/contacts/remove` |

### Emails

| Action | Method | Endpoint |
|--------|--------|----------|
| Send transactional | POST | `/smtp/email` |
| Send campaign | POST | `/emailCampaigns` |
| Get templates | GET | `/smtp/templates` |

## Examples

### Create/Update Contact

```bash
curl -X POST "https://api.brevo.com/v3/contacts" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "listIds": [10],
    "updateEnabled": true,
    "attributes": {
      "NOMBRE": "John",
      "APELLIDOS": "Doe"
    }
  }'
```

### Get Contact Info

```bash
curl "https://api.brevo.com/v3/contacts/user@example.com" \
  -H "api-key: $BREVO_KEY"
```

### Update Contact Attributes

```bash
curl -X PUT "https://api.brevo.com/v3/contacts/user@example.com" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "listIds": [10, 15],
    "attributes": {
      "CUSTOM_FIELD": "value"
    }
  }'
```

### Send Transactional Email

```bash
curl -X POST "https://api.brevo.com/v3/smtp/email" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": {"name": "My App", "email": "noreply@example.com"},
    "to": [{"email": "user@example.com", "name": "John"}],
    "subject": "Welcome!",
    "htmlContent": "<p>Hello {{params.name}}</p>",
    "params": {"name": "John"}
  }'
```

### Send with Template

```bash
curl -X POST "https://api.brevo.com/v3/smtp/email" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": [{"email": "user@example.com"}],
    "templateId": 34,
    "params": {
      "NOMBRE": "John",
      "FECHA": "2026-02-01"
    }
  }'
```

### List All Contact Lists

```bash
curl "https://api.brevo.com/v3/contacts/lists?limit=50" \
  -H "api-key: $BREVO_KEY"
```

### Add Contacts to List (Bulk)

```bash
curl -X POST "https://api.brevo.com/v3/contacts/lists/10/contacts/add" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "emails": ["user1@example.com", "user2@example.com"]
  }'
```

## Safe Import Pattern

When importing contacts, **always respect unsubscribes**:

```python
import requests

BREVO_KEY = "your-api-key"
HEADERS = {'api-key': BREVO_KEY, 'Content-Type': 'application/json'}
BASE = 'https://api.brevo.com/v3'

def get_blacklisted():
    """Get all unsubscribed/blacklisted emails"""
    blacklisted = set()
    offset = 0
    while True:
        r = requests.get(
            f'{BASE}/contacts?limit=100&offset={offset}&emailBlacklisted=true',
            headers=HEADERS
        )
        contacts = r.json().get('contacts', [])
        if not contacts:
            break
        for c in contacts:
            blacklisted.add(c['email'].lower())
        offset += 100
    return blacklisted

def safe_import(emails, list_id):
    """Import contacts respecting unsubscribes"""
    blacklisted = get_blacklisted()
    
    for email in emails:
        if email.lower() in blacklisted:
            print(f"Skipped (unsubscribed): {email}")
            continue
        
        r = requests.post(f'{BASE}/contacts', headers=HEADERS, json={
            'email': email,
            'listIds': [list_id],
            'updateEnabled': True
        })
        
        if r.status_code in [200, 201, 204]:
            print(f"Imported: {email}")
        else:
            print(f"Error: {email} - {r.text[:50]}")
```

## Contact Attributes

Brevo uses custom attributes for contact data:

```json
{
  "attributes": {
    "NOMBRE": "John",
    "APELLIDOS": "Doe",
    "FECHA_ALTA": "2026-01-15",
    "PLAN": "premium",
    "CUSTOM_FIELD": "any value"
  }
}
```

Create attributes in Brevo dashboard: Contacts → Settings → Contact attributes.

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success (GET) |
| 201 | Created (POST) |
| 204 | Success, no content (PUT/DELETE) |
| 400 | Bad request (check payload) |
| 401 | Invalid API key |
| 404 | Contact/resource not found |

## Best Practices

1. **Always check blacklist** before importing contacts
2. **Use `updateEnabled: true`** to update existing contacts instead of failing
3. **Use templates** for consistent transactional emails
4. **Batch operations** when adding many contacts to lists
5. **Store list IDs** in config, not hardcoded
6. **Log imports** for audit trail

## Automations

Brevo automations trigger on:
- Contact added to list
- Contact attribute updated
- Email opened/clicked
- Custom events via API

Trigger automation manually:
```bash
curl -X POST "https://api.brevo.com/v3/contacts/import" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "listIds": [10],
    "emailBlacklist": false,
    "updateExistingContacts": true,
    "emptyContactsAttributes": false,
    "jsonBody": [
      {"email": "user@example.com", "attributes": {"NOMBRE": "John"}}
    ]
  }'
```

## Useful Queries

```bash
# Count contacts in list
curl "https://api.brevo.com/v3/contacts/lists/10" -H "api-key: $BREVO_KEY" | jq '.totalSubscribers'

# Get recent contacts
curl "https://api.brevo.com/v3/contacts?limit=10&sort=desc" -H "api-key: $BREVO_KEY"

# Check if email exists
curl "https://api.brevo.com/v3/contacts/user@example.com" -H "api-key: $BREVO_KEY"

# Get account info
curl "https://api.brevo.com/v3/account" -H "api-key: $BREVO_KEY"
```
