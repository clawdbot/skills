---
name: nocodb
description: Access and manage NocoDB databases, tables, and records via REST API. Use when the user wants to view bases, list tables, inspect column schemas, query or filter row data, or insert new records into a self-hosted NocoDB instance. Also use for spreadsheet-style database lookups and data entry.
---

# NocoDB

Manage bases, tables, and rows on a self-hosted NocoDB instance via REST API.

## Setup

```bash
export NOCODB_URL="https://your-nocodb-instance.com"
export NOCODB_TOKEN="your-api-token"
```

Get your API token: NocoDB → Team & Settings → API Tokens → Add New Token.

## Commands

### List bases

```bash
{baseDir}/scripts/nocodb.sh bases
```

### List tables in a base

```bash
{baseDir}/scripts/nocodb.sh tables --base "Library"
{baseDir}/scripts/nocodb.sh tables --base pz38oanbzcaqfae
```

Base and table args accept names (case-insensitive) or IDs.

### Show columns (schema)

```bash
{baseDir}/scripts/nocodb.sh columns --base "Library" --table "Books"
```

### Query rows

```bash
{baseDir}/scripts/nocodb.sh rows --base "Library" --table "Books" --limit 10
{baseDir}/scripts/nocodb.sh rows --base "Library" --table "Books" --sort "-CreatedAt"
{baseDir}/scripts/nocodb.sh rows --base "Library" --table "Books" --where "(Title,like,%Preparation%)"
{baseDir}/scripts/nocodb.sh rows --base "Library" --table "Books" --limit 5 --offset 10
```

Sort: prefix with `-` for descending. Where: NocoDB filter syntax `(Field,op,value)`.

### Get single row

```bash
{baseDir}/scripts/nocodb.sh row --base "Library" --table "Books" --id 1
```

### Insert a row

```bash
{baseDir}/scripts/nocodb.sh insert --base "Library" --table "Books" --json '{"Title": "New Book", "Publish Date": 2026}'
```

Pass field values as a JSON object. Check columns first to see available fields.

## Filter Operators

Common NocoDB where operators: `eq`, `neq`, `like`, `gt`, `lt`, `gte`, `lte`, `is`, `isnot`, `null`, `notnull`.

Combine filters: `(Field1,eq,val1)~and(Field2,gt,val2)`
