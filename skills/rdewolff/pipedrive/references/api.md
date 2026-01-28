# Pipedrive API Reference

Base URL: `https://api.pipedrive.com/v1`  
Auth: `api_token` query parameter

## Deals

### List Deals
```
GET /deals
Query: limit, start, status (open|won|lost|deleted), stage_id, user_id, filter_id, sort
```

### Search Deals
```
GET /itemSearch?term=QUERY&item_types=deal
Query: term (search query), item_types, limit, start
```

### Get Deal
```
GET /deals/{id}
```

### Create Deal
```
POST /deals
Body: {
  "title": "Deal Title",           // required
  "value": 1000,                   // optional
  "currency": "USD",               // optional, default from settings
  "person_id": 123,                // optional
  "org_id": 456,                   // optional
  "pipeline_id": 1,                // optional, default pipeline if omitted
  "stage_id": 1,                   // optional, first stage of pipeline
  "status": "open",                // optional: open|won|lost
  "expected_close_date": "2024-12-31",  // optional
  "probability": 50,               // optional, 0-100
  "lost_reason": "Reason text",    // optional, for lost deals
  "visible_to": "3"                // optional: 1=owner, 3=entire company
}
```

### Update Deal
```
PUT /deals/{id}
Body: (same as create, partial update)
```

### Delete Deal
```
DELETE /deals/{id}
```

### Deal Timeline
```
GET /deals/timeline
Query: start_date, interval, amount, field_key, pipeline_id, filter_id
```

## Persons (Contacts)

### List Persons
```
GET /persons
Query: limit, start, sort, filter_id
```

### Search Persons
```
GET /itemSearch?term=QUERY&item_types=person
```

### Get Person
```
GET /persons/{id}
```

### Create Person
```
POST /persons
Body: {
  "name": "John Doe",              // required
  "email": [                        // optional, array format
    {"value": "john@example.com", "primary": true, "label": "work"}
  ],
  "phone": [                        // optional, array format
    {"value": "+1234567890", "primary": true, "label": "work"}
  ],
  "org_id": 123,                   // optional
  "visible_to": "3"                // optional
}
```

### Update Person
```
PUT /persons/{id}
Body: (same as create, partial update)
```

### Delete Person
```
DELETE /persons/{id}
```

### Get Person Deals
```
GET /persons/{id}/deals
Query: limit, start, status
```

## Organizations

### List Organizations
```
GET /organizations
Query: limit, start, sort, filter_id
```

### Search Organizations
```
GET /itemSearch?term=QUERY&item_types=organization
```

### Get Organization
```
GET /organizations/{id}
```

### Create Organization
```
POST /organizations
Body: {
  "name": "Acme Corp",             // required
  "address": "123 Main St",        // optional
  "visible_to": "3"                // optional
}
```

### Update Organization
```
PUT /organizations/{id}
Body: (same as create, partial update)
```

### Delete Organization
```
DELETE /organizations/{id}
```

### Get Organization Persons
```
GET /organizations/{id}/persons
Query: limit, start
```

### Get Organization Deals
```
GET /organizations/{id}/deals
Query: limit, start, status
```

## Activities

### List Activities
```
GET /activities
Query: limit, start, done (0|1), type, user_id, deal_id, person_id, org_id
```

### Get Activity
```
GET /activities/{id}
```

### Create Activity
```
POST /activities
Body: {
  "subject": "Call with client",   // required
  "type": "call",                  // required: call|meeting|task|deadline|email|lunch
  "due_date": "2024-01-15",        // required: YYYY-MM-DD
  "due_time": "14:00",             // optional: HH:MM
  "duration": "00:30:00",          // optional: HH:MM:SS
  "deal_id": 123,                  // optional
  "person_id": 456,                // optional
  "org_id": 789,                   // optional
  "note": "Notes about activity",  // optional
  "location": "Office",            // optional
  "done": 0,                       // optional: 0|1
  "busy_flag": true                // optional, for calendar blocking
}
```

### Update Activity
```
PUT /activities/{id}
Body: (same as create, partial update)
```

### Delete Activity
```
DELETE /activities/{id}
```

### Activity Types
```
GET /activityTypes
Returns: List of available activity types (call, meeting, task, etc.)
```

## Pipelines

### List Pipelines
```
GET /pipelines
```

### Get Pipeline
```
GET /pipelines/{id}
```

### Get Pipeline Deals
```
GET /pipelines/{id}/deals
Query: limit, start, status, filter_id
```

## Stages

### List Stages
```
GET /stages
Query: pipeline_id (optional, filter by pipeline)
```

### Get Stage
```
GET /stages/{id}
```

### Get Stage Deals
```
GET /stages/{id}/deals
Query: limit, start, filter_id
```

## Leads

### List Leads
```
GET /leads
Query: limit, start, sort, archived_status
```

### Get Lead
```
GET /leads/{id}
```

### Create Lead
```
POST /leads
Body: {
  "title": "New Lead",             // required
  "person_id": "uuid-string",      // optional (UUID format)
  "organization_id": "uuid-string", // optional (UUID format)
  "value": {                       // optional
    "amount": 1000,
    "currency": "USD"
  },
  "expected_close_date": "2024-12-31",  // optional
  "label_ids": ["uuid1", "uuid2"], // optional
  "visible_to": "3"                // optional
}
Note: Lead IDs are UUIDs, not integers like other resources
```

### Update Lead
```
PATCH /leads/{id}
Body: (same as create, partial update)
```

### Delete Lead
```
DELETE /leads/{id}
```

## Products

### List Products
```
GET /products
Query: limit, start
```

### Search Products
```
GET /itemSearch?term=QUERY&item_types=product
```

### Get Product
```
GET /products/{id}
```

### Create Product
```
POST /products
Body: {
  "name": "Product Name",          // required
  "code": "PROD-001",              // optional
  "unit": "piece",                 // optional
  "prices": [                      // optional
    {"price": 100, "currency": "USD", "cost": 50}
  ],
  "active_flag": true              // optional
}
```

### Deal Products
```
GET /deals/{id}/products           // List products attached to deal
POST /deals/{id}/products          // Add product to deal
PUT /deals/{id}/products/{product_attachment_id}  // Update attached product
DELETE /deals/{id}/products/{product_attachment_id}  // Remove product from deal
```

## Notes

### List Notes
```
GET /notes
Query: limit, start, deal_id, person_id, org_id, sort
```

### Get Note
```
GET /notes/{id}
```

### Create Note
```
POST /notes
Body: {
  "content": "Note content",       // required
  "deal_id": 123,                  // optional
  "person_id": 456,                // optional
  "org_id": 789,                   // optional
  "pinned_to_deal_flag": 0,        // optional: 0|1
  "pinned_to_person_flag": 0,      // optional: 0|1
  "pinned_to_organization_flag": 0 // optional: 0|1
}
Note: At least one of deal_id, person_id, or org_id is required
```

### Update Note
```
PUT /notes/{id}
Body: (same as create, partial update)
```

### Delete Note
```
DELETE /notes/{id}
```

## Item Search (Universal)

```
GET /itemSearch
Query:
  term: Search query (required)
  item_types: Comma-separated: deal,person,organization,product,file
  exact_match: true/false
  limit: Max results
  start: Offset
  
Response includes:
  - data.items[].item.id
  - data.items[].item.type
  - data.items[].item.title/name
  - data.items[].result_score
```

## Pagination

All list endpoints support:
- `limit` - Max results per page (default: 100, max: 500)
- `start` - Offset for pagination (0-indexed)

Response includes:
```json
{
  "success": true,
  "data": [...],
  "additional_data": {
    "pagination": {
      "start": 0,
      "limit": 100,
      "more_items_in_collection": true,
      "next_start": 100
    }
  }
}
```

## Rate Limiting

- 10 requests/second per API token
- 100,000 requests/day per company
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- 429 Too Many Requests when exceeded

## Error Responses

```json
{
  "success": false,
  "error": "Error message",
  "error_info": "Additional details",
  "data": null
}
```

Common errors:
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (invalid API token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource doesn't exist)
- 429: Rate Limited
- 500: Internal Server Error

## Deal Statuses

| Status | Description |
|--------|-------------|
| `open` | Active deal in pipeline |
| `won` | Deal closed successfully |
| `lost` | Deal lost/rejected |
| `deleted` | Deal was deleted |

## Activity Types

Default types (can be customized):
- `call` - Phone call
- `meeting` - Meeting
- `task` - Task
- `deadline` - Deadline
- `email` - Email
- `lunch` - Lunch meeting

## Visibility Levels

| Value | Description |
|-------|-------------|
| `1` | Owner only |
| `3` | Entire company |
| `5` | Owner's visibility group |
| `7` | Owner's visibility group + sub-groups |

## Webhooks (for reference)

```
GET /webhooks            - List webhooks
POST /webhooks           - Create webhook
DELETE /webhooks/{id}    - Delete webhook

Events: added, updated, merged, deleted
Objects: deal, person, organization, activity, note, pipeline, stage, user
```

## Users (for reference)

```
GET /users               - List users
GET /users/{id}          - Get user
GET /users/me            - Get current user
```

## Filters (for reference)

```
GET /filters             - List filters
GET /filters/{id}        - Get filter details
```

Filters can be applied to list endpoints via `filter_id` parameter.
