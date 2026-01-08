---
name: frappecli
version: 0.1.0
description: CLI for Frappe Framework / ERPNext instances. Use when user asks about "Frappe", "ERPNext", "doctypes", "Frappe API", or needs to manage documents, files, reports, or call RPC methods on a Frappe site.
tools: [bash]
---

# frappecli

CLI for managing Frappe Framework instances via REST API.

## Installation

```bash
brew tap pasogott/tap
brew install frappecli
```

Or from source:
```bash
git clone https://github.com/pasogott/frappecli.git
cd frappecli && uv sync && uv pip install -e .
```

## Configuration

Create `~/.config/frappecli/config.yaml`:

```yaml
sites:
  production:
    url: https://erp.company.com
    api_key: your_api_key
    api_secret: your_api_secret
  staging:
    url: https://staging.company.com
    api_key: your_staging_key
    api_secret: your_staging_secret

default_site: production
```

## Commands

### Site Management
```bash
frappecli site doctypes                    # List all doctypes
frappecli site doctypes --module "Core"    # Filter by module
frappecli site info "User"                 # Get doctype details
```

### Document CRUD
```bash
# List documents
frappecli doc list Customer
frappecli doc list Customer --filters '{"status":"Active"}' --limit 10

# Get single document
frappecli doc get Customer CUST-001
frappecli doc get Customer CUST-001 --fields name,customer_name,status

# Create document
frappecli doc create Customer --data '{"customer_name":"Acme","customer_type":"Company"}'

# Update document
frappecli doc update Customer CUST-001 --data '{"status":"Inactive"}'

# Delete document
frappecli doc delete Customer CUST-001
```

### File Management
```bash
# Upload file (private by default)
frappecli file upload invoice.pdf --doctype "Sales Invoice" --docname "INV-001"

# Upload public file
frappecli file upload logo.png --public

# Download file
frappecli file download /private/files/invoice.pdf -o ./downloads/

# List files for document
frappecli file list --doctype "Sales Invoice" --docname "INV-001"
```

### Reports
```bash
# Run report (JSON output)
frappecli report run "General Ledger" --filters '{"company":"My Company"}'

# Export to CSV
frappecli report run "Accounts Receivable" --format csv -o report.csv
```

### RPC Methods
```bash
# Call custom method
frappecli rpc frappe.ping

# With arguments
frappecli rpc myapp.api.process_data --args '{"doc_id":"DOC-001"}'
```

### Multi-Site
```bash
# Use specific site
frappecli --site staging doc list Customer

# Switch default site
frappecli config set default_site staging
```

## Output Formats

```bash
frappecli doc list Customer --format table   # Pretty table (default)
frappecli doc list Customer --format json    # JSON
frappecli doc list Customer --format csv     # CSV
```

## Examples

### Bulk Operations
```bash
# Export all active customers
frappecli doc list Customer --filters '{"status":"Active"}' --format csv > customers.csv

# Get document with child tables
frappecli doc get "Sales Invoice" INV-001 --fields '*'
```

### Integration with jq
```bash
# Get customer names only
frappecli doc list Customer --format json | jq -r '.[].customer_name'

# Count by status
frappecli doc list Customer --format json | jq 'group_by(.status) | map({status: .[0].status, count: length})'
```

## Links

- **Repository:** https://github.com/pasogott/frappecli
- **Homebrew:** `brew install pasogott/tap/frappecli`
