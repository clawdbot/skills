---
name: salesforce
description: "Query and manage Salesforce CRM data via the Salesforce CLI (`sf`). Run SOQL/SOSL queries, inspect object schemas, create/update/delete records, bulk import/export, execute Apex, deploy metadata, and make raw REST API calls."
homepage: https://developer.salesforce.com/tools/salesforcecli
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["sf"]},"install":[{"id":"npm","kind":"node","package":"@salesforce/cli","bins":["sf"],"label":"Install Salesforce CLI (npm)"}]}}
---

# Salesforce Skill

Use the Salesforce CLI (`sf`) to interact with Salesforce orgs. The CLI must be authenticated before use. Always add `--json` for structured output.

If the `sf` binary is not available, install it via npm (`npm install -g @salesforce/cli`) or download it from https://developer.salesforce.com/tools/salesforcecli. After installing, authenticate immediately with `sf org login web` to connect to a Salesforce org.

## Authentication and Org Management

### Log in (opens browser)
```bash
sf org login web --alias my-org
```

Other login methods:
```bash
# JWT-based login (CI/automation)
sf org login jwt --client-id <consumer-key> --jwt-key-file server.key --username user@example.com --alias my-org

# Login with an existing access token
sf org login access-token --instance-url https://mycompany.my.salesforce.com

# Login via SFDX auth URL (from a file)
sf org login sfdx-url --sfdx-url-file authUrl.txt --alias my-org
```

### Manage orgs
```bash
# List all authenticated orgs
sf org list --json

# Display info about the default org (access token, instance URL, username)
sf org display --json

# Display info about a specific org
sf org display --target-org my-org --json

# Display with SFDX auth URL (sensitive - contains refresh token)
sf org display --target-org my-org --verbose --json

# Open org in browser
sf org open
sf org open --target-org my-org

# Log out
sf org logout --target-org my-org
```

### Configuration and aliases
```bash
# Set default target org
sf config set target-org my-org

# List all config variables
sf config list

# Get a specific config value
sf config get target-org

# Set an alias
sf alias set prod=user@example.com

# List aliases
sf alias list
```

## Querying Data (SOQL)

Standard SOQL queries via the default API:
```bash
# Basic query
sf data query --query "SELECT Id, Name, Email FROM Contact LIMIT 10" --json

# WHERE clause
sf data query --query "SELECT Id, Name, Amount, StageName FROM Opportunity WHERE StageName = 'Closed Won'" --json

# Relationship queries (parent-to-child)
sf data query --query "SELECT Id, Name, (SELECT LastName, Email FROM Contacts) FROM Account LIMIT 5" --json

# Relationship queries (child-to-parent)
sf data query --query "SELECT Id, Name, Account.Name FROM Contact" --json

# LIKE for text search
sf data query --query "SELECT Id, Name FROM Account WHERE Name LIKE '%Acme%'" --json

# Date filtering
sf data query --query "SELECT Id, Name, CreatedDate FROM Lead WHERE CreatedDate = TODAY" --json

# ORDER BY + LIMIT
sf data query --query "SELECT Id, Name, Amount FROM Opportunity ORDER BY Amount DESC LIMIT 20" --json

# Include deleted/archived records
sf data query --query "SELECT Id, Name FROM Account" --all-rows --json

# Query from a file
sf data query --file query.soql --json

# Tooling API queries (metadata objects like ApexClass, ApexTrigger)
sf data query --query "SELECT Id, Name, Status FROM ApexClass" --use-tooling-api --json

# Output to CSV file
sf data query --query "SELECT Id, Name, Email FROM Contact" --result-format csv --output-file contacts.csv

# Target a specific org
sf data query --query "SELECT Id, Name FROM Account" --target-org my-org --json
```

For queries returning more than 10,000 records, use Bulk API instead:
```bash
sf data export bulk --query "SELECT Id, Name, Email FROM Contact" --output-file contacts.csv --result-format csv --wait 10
sf data export bulk --query "SELECT Id, Name FROM Account" --output-file accounts.json --result-format json --wait 10
```

## Text Search (SOSL)

SOSL searches across multiple objects at once:
```bash
# Search for text across objects
sf data search --query "FIND {John Smith} IN ALL FIELDS RETURNING Contact(Name, Email), Lead(Name, Email)" --json

# Search in name fields only
sf data search --query "FIND {Acme} IN NAME FIELDS RETURNING Account(Name, Industry), Contact(Name)" --json

# Search from a file
sf data search --file search.sosl --json

# Output to CSV
sf data search --query "FIND {test} RETURNING Contact(Name)" --result-format csv
```

## Single Record Operations

### Get a record
```bash
# By record ID
sf data get record --sobject Contact --record-id 003XXXXXXXXXXXX --json

# By field match (WHERE-like)
sf data get record --sobject Account --where "Name=Acme" --json

# By multiple fields (values with spaces need single quotes)
sf data get record --sobject Account --where "Name='Universal Containers' Phone='(123) 456-7890'" --json
```

### Create a record (confirm with user first)
```bash
sf data create record --sobject Contact --values "FirstName='Jane' LastName='Doe' Email='jane@example.com'" --json

sf data create record --sobject Account --values "Name='New Company' Website=www.example.com Industry='Technology'" --json

# Tooling API object
sf data create record --sobject TraceFlag --use-tooling-api --values "DebugLevelId=7dl... LogType=CLASS_TRACING" --json
```

### Update a record (confirm with user first)
```bash
# By ID
sf data update record --sobject Contact --record-id 003XXXXXXXXXXXX --values "Email='updated@example.com'" --json

# By field match
sf data update record --sobject Account --where "Name='Old Acme'" --values "Name='New Acme'" --json

# Multiple fields
sf data update record --sobject Account --record-id 001XXXXXXXXXXXX --values "Name='Acme III' Website=www.example.com" --json
```

### Delete a record (require explicit user confirmation)
```bash
# By ID
sf data delete record --sobject Account --record-id 001XXXXXXXXXXXX --json

# By field match
sf data delete record --sobject Account --where "Name=Acme" --json
```

## Bulk Data Operations (Bulk API 2.0)

For large datasets (thousands to millions of records):

### Bulk export
```bash
# Export to CSV
sf data export bulk --query "SELECT Id, Name, Email FROM Contact" --output-file contacts.csv --result-format csv --wait 10

# Export to JSON
sf data export bulk --query "SELECT Id, Name FROM Account" --output-file accounts.json --result-format json --wait 10

# Include soft-deleted records
sf data export bulk --query "SELECT Id, Name FROM Account" --output-file accounts.csv --result-format csv --all-rows --wait 10

# Resume a timed-out export
sf data export resume --job-id 750XXXXXXXXXXXX --json
```

### Bulk import
```bash
# Import from CSV
sf data import bulk --file accounts.csv --sobject Account --wait 10

# Resume a timed-out import
sf data import resume --job-id 750XXXXXXXXXXXX --json
```

### Bulk upsert
```bash
sf data upsert bulk --file contacts.csv --sobject Contact --external-id Email --wait 10
```

### Bulk delete
```bash
# Delete records listed in CSV (CSV must have an Id column)
sf data delete bulk --file records-to-delete.csv --sobject Contact --wait 10
```

### Tree export/import (for related records)
```bash
# Export with relationships into JSON tree format
sf data export tree --query "SELECT Id, Name, (SELECT Name, Email FROM Contacts) FROM Account" --json

# Export with a plan file (for multiple objects)
sf data export tree --query "SELECT Id, Name FROM Account" --plan --output-dir export-data

# Import from tree JSON files
sf data import tree --files Account.json,Contact.json

# Import using a plan definition file
sf data import tree --plan Account-Contact-plan.json
```

## Schema Inspection

```bash
# Describe an object (fields, relationships, picklist values)
sf sobject describe --sobject Account --json

# Describe a custom object
sf sobject describe --sobject MyCustomObject__c --json

# Describe a Tooling API object
sf sobject describe --sobject ApexClass --use-tooling-api --json

# List all objects
sf sobject list --json

# List only custom objects
sf sobject list --sobject custom --json

# List only standard objects
sf sobject list --sobject standard --json
```

## Execute Apex Code

```bash
# Execute Apex from a file
sf apex run --file script.apex --json

# Run interactively (type code, press Ctrl+D to execute)
sf apex run

# Run Apex tests
sf apex run test --test-names MyTestClass --json

# Get test results
sf apex get test --test-run-id 707XXXXXXXXXXXX --json

# View Apex logs
sf apex list log --json
sf apex get log --log-id 07LXXXXXXXXXXXX
```

## REST API (Advanced)

Make arbitrary authenticated REST API calls:
```bash
# GET request
sf api request rest 'services/data/v62.0/limits' --json

# List API versions
sf api request rest '/services/data/' --json

# Create a record via REST
sf api request rest '/services/data/v62.0/sobjects/Account' --method POST --body '{"Name":"REST Account","Industry":"Technology"}' --json

# Update a record via REST (PATCH)
sf api request rest '/services/data/v62.0/sobjects/Account/001XXXXXXXXXXXX' --method PATCH --body '{"BillingCity":"San Francisco"}' --json

# GraphQL query
sf api request graphql --body '{"query":"{ uiapi { query { Account { edges { node { Name { value } } } } } } }"}' --json

# Custom headers
sf api request rest '/services/data/v62.0/limits' --header 'Accept: application/xml'

# Save response to file
sf api request rest '/services/data/v62.0/limits' --stream-to-file limits.json
```

## Metadata Deployment and Retrieval

```bash
# Deploy metadata to an org
sf project deploy start --source-dir force-app --json

# Deploy specific metadata components
sf project deploy start --metadata ApexClass:MyClass --json

# Retrieve metadata from an org
sf project retrieve start --metadata ApexClass --json

# Check deploy status
sf project deploy report --job-id 0AfXXXXXXXXXXXX --json

# Generate a new Salesforce DX project
sf project generate --name my-project

# List metadata components in the org
sf project list ignored --json
```

## Diagnostics

```bash
# Run CLI diagnostics
sf doctor

# Check CLI version
sf version

# See what is new
sf whatsnew
```

## Common SOQL Patterns

```sql
-- Count records
SELECT COUNT() FROM Contact WHERE AccountId = '001XXXXXXXXXXXX'

-- Aggregate query
SELECT StageName, COUNT(Id), SUM(Amount) FROM Opportunity GROUP BY StageName

-- Date literals
SELECT Id, Name FROM Lead WHERE CreatedDate = LAST_N_DAYS:30

-- Subquery (semi-join)
SELECT Id, Name FROM Account WHERE Id IN (SELECT AccountId FROM Contact WHERE Email LIKE '%@acme.com')

-- Polymorphic lookup
SELECT Id, Who.Name, Who.Type FROM Task WHERE Who.Type = 'Contact'

-- Multiple WHERE conditions
SELECT Id, Name, Amount FROM Opportunity WHERE Amount > 10000 AND StageName != 'Closed Lost' AND CloseDate = THIS_QUARTER
```

## Guardrails

- **Always use `--json`** for structured, parseable output.
- **Never create, update, or delete records** without explicit user confirmation. Describe the operation and ask before executing.
- **Never delete records** unless the user explicitly requests it and confirms the specific record(s).
- **Never bulk delete or bulk import** without user reviewing the file/query and confirming.
- Use `LIMIT` on queries to avoid excessive data. Start with `LIMIT 10` and increase if the user needs more.
- For queries over 10,000 records, use `sf data export bulk` instead of `sf data query`.
- When the user asks to "find" or "search" a single object, use SOQL `WHERE ... LIKE '%term%'`. When searching across multiple objects, use SOSL via `sf data search`.
- Use `--target-org <alias>` when the user has multiple orgs; ask which org if ambiguous.
- If authentication fails or a session expires, guide the user through `sf org login web`.
- Bulk API 2.0 has SOQL limitations (no aggregate functions like `COUNT()`). Use standard `sf data query` for those.
- When describing objects (`sf sobject describe`), the JSON output can be very large. Summarize the key fields, required fields, and relationships for the user rather than dumping the raw output.
