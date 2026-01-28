#!/bin/bash
# Pipedrive CRM API CLI
# Usage: pipedrive.sh <resource> <command> [args...]

set -e

# Show help if no args
if [ -z "$1" ]; then
  echo "Pipedrive CRM CLI"
  echo ""
  echo "Resources:"
  echo "  deals       Manage deals (list, search, show, create, update, won, lost, delete)"
  echo "  persons     Manage contacts (list, search, show, create, update, delete)"
  echo "  orgs        Manage organizations (list, search, show, create, update, delete)"
  echo "  activities  Manage activities (list, show, create, done)"
  echo "  pipelines   View pipelines and stages (list, stages)"
  echo "  leads       Manage leads (list, show, create, convert)"
  echo "  products    View products (list, search)"
  echo "  notes       Manage notes (list, create)"
  echo ""
  echo "Usage: pipedrive.sh <resource> <command> [options]"
  echo ""
  echo "Examples:"
  echo "  pipedrive.sh deals list"
  echo "  pipedrive.sh deals search \"Acme\""
  echo "  pipedrive.sh persons create --name \"John Doe\" --email \"john@example.com\""
  exit 0
fi

# Get API token from env or clawdbot config
if [ -z "$PIPEDRIVE_API_TOKEN" ]; then
  PIPEDRIVE_API_TOKEN=$(python3 -c "
import json
try:
    with open('$HOME/.clawdbot/clawdbot.json') as f:
        cfg = json.load(f)
    token = cfg.get('skills', {}).get('entries', {}).get('pipedrive', {}).get('apiToken', '')
    print(token)
except: pass
" 2>/dev/null || echo "")
fi

if [ -z "$PIPEDRIVE_API_TOKEN" ]; then
  echo "Error: PIPEDRIVE_API_TOKEN not set."
  echo "Configure in ~/.clawdbot/clawdbot.json under skills.entries.pipedrive.apiToken"
  echo "Or set env var PIPEDRIVE_API_TOKEN"
  exit 1
fi

API_URL="https://api.pipedrive.com/v1"

# Helper function for API calls
pipedrive_api() {
  local method="$1"
  local endpoint="$2"
  local data="$3"
  
  # Add api_token to URL
  if [[ "$endpoint" == *"?"* ]]; then
    local url="$API_URL$endpoint&api_token=$PIPEDRIVE_API_TOKEN"
  else
    local url="$API_URL$endpoint?api_token=$PIPEDRIVE_API_TOKEN"
  fi
  
  if [ -n "$data" ]; then
    curl -s -X "$method" "$url" \
      -H "Accept: application/json" \
      -H "Content-Type: application/json" \
      -d "$data"
  else
    curl -s -X "$method" "$url" \
      -H "Accept: application/json"
  fi
}

# Check API response for errors
check_error() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success', True):
    err = data.get('error', 'Unknown error')
    print(f'❌ Error: {err}', file=sys.stderr)
    sys.exit(1)
print(json.dumps(data))
"
}

# Format deals output
format_deals() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
deals = data.get('data') or []
if not deals:
    print('No deals found.')
    sys.exit(0)
for d in deals:
    status_icon = {'open': '🔵', 'won': '✅', 'lost': '❌', 'deleted': '🗑️'}.get(d.get('status', ''), '❓')
    title = (d.get('title') or 'Untitled')[:40]
    value = d.get('value') or 0
    currency = d.get('currency') or ''
    person = d.get('person_name') or ''
    org = d.get('org_name') or ''
    stage = d.get('stage_id', '-')
    print(f\"{status_icon} {d.get('id')}\t{title}\t{value} {currency}\t{person[:20]}\t{org[:20]}\")
"
}

# Format persons output
format_persons() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
persons = data.get('data') or []
if not persons:
    print('No persons found.')
    sys.exit(0)
for p in persons:
    name = (p.get('name') or 'Unknown')[:35]
    # Handle email array
    emails = p.get('email') or []
    email = ''
    if isinstance(emails, list) and emails:
        email = emails[0].get('value', '') if isinstance(emails[0], dict) else str(emails[0])
    elif isinstance(emails, str):
        email = emails
    org = ''
    if p.get('org_name'):
        org = p.get('org_name')
    elif p.get('org_id') and isinstance(p.get('org_id'), dict):
        org = p.get('org_id', {}).get('name', '')
    print(f\"👤 {p.get('id')}\t{name}\t{email[:30]}\t{org[:25]}\")
"
}

# Format organizations output
format_orgs() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
orgs = data.get('data') or []
if not orgs:
    print('No organizations found.')
    sys.exit(0)
for o in orgs:
    name = (o.get('name') or 'Unknown')[:40]
    address = (o.get('address') or '')[:30]
    people = o.get('people_count', 0)
    deals_open = o.get('open_deals_count', 0)
    deals_won = o.get('won_deals_count', 0)
    print(f\"🏢 {o.get('id')}\t{name}\t{address}\t{people}p\t{deals_open}o/{deals_won}w\")
"
}

# Format activities output
format_activities() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
activities = data.get('data') or []
if not activities:
    print('No activities found.')
    sys.exit(0)
for a in activities:
    done_icon = '✅' if a.get('done') else '⏳'
    subject = (a.get('subject') or 'No subject')[:40]
    atype = a.get('type') or ''
    due_date = a.get('due_date') or ''
    due_time = a.get('due_time') or ''
    deal = a.get('deal_title') or ''
    print(f\"{done_icon} {a.get('id')}\t{atype[:10]}\t{due_date} {due_time}\t{subject}\t{deal[:20]}\")
"
}

# Format pipelines output
format_pipelines() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
pipelines = data.get('data') or []
if not pipelines:
    print('No pipelines found.')
    sys.exit(0)
for p in pipelines:
    name = (p.get('name') or 'Unnamed')[:40]
    active = '🟢' if p.get('active') else '⚪'
    deals = p.get('deals_count', 0)
    print(f\"{active} {p.get('id')}\t{name}\t{deals} deals\")
"
}

# Format stages output
format_stages() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
stages = data.get('data') or []
if not stages:
    print('No stages found.')
    sys.exit(0)
for s in stages:
    name = (s.get('name') or 'Unnamed')[:35]
    order = s.get('order_nr', 0)
    deals = s.get('deals_count', 0) if 'deals_count' in s else '-'
    rotten = '⚠️' if s.get('rotten_flag') else ''
    print(f\"  {order}. {s.get('id')}\t{name}\t{deals} deals {rotten}\")
"
}

# Format leads output
format_leads() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
leads = data.get('data') or []
if not leads:
    print('No leads found.')
    sys.exit(0)
for l in leads:
    title = (l.get('title') or 'Untitled')[:40]
    # Value might be dict with amount/currency
    value = l.get('value') or {}
    if isinstance(value, dict):
        amt = value.get('amount', 0)
        cur = value.get('currency', '')
        value_str = f\"{amt} {cur}\"
    else:
        value_str = str(value)
    person_id = l.get('person_id') or '-'
    org_id = l.get('organization_id') or '-'
    print(f\"💡 {l.get('id')}\t{title}\t{value_str}\tP:{person_id}\tO:{org_id}\")
"
}

# Format products output
format_products() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
products = data.get('data') or []
if not products:
    print('No products found.')
    sys.exit(0)
for p in products:
    name = (p.get('name') or 'Unknown')[:40]
    code = p.get('code') or ''
    # Get first price
    prices = p.get('prices') or []
    price_str = ''
    if prices:
        pr = prices[0]
        price_str = f\"{pr.get('price', 0)} {pr.get('currency', '')}\"
    active = '🟢' if p.get('active_flag') else '⚪'
    print(f\"{active} {p.get('id')}\t{name}\t{code[:15]}\t{price_str}\")
"
}

# Format notes output
format_notes() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
notes = data.get('data') or []
if not notes:
    print('No notes found.')
    sys.exit(0)
for n in notes:
    content = (n.get('content') or '')[:60].replace('\n', ' ')
    add_time = (n.get('add_time') or '')[:10]
    pinned = '📌' if n.get('pinned_to_deal_flag') or n.get('pinned_to_person_flag') or n.get('pinned_to_organization_flag') else ''
    deal = n.get('deal_id') or '-'
    person = n.get('person_id') or '-'
    org = n.get('org_id') or '-'
    print(f\"📝 {n.get('id')}\t{add_time}\t{pinned}{content}\")
"
}

# Show detailed deal
show_deal() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
d = data.get('data', {})
status_icon = {'open': '🔵 Open', 'won': '✅ Won', 'lost': '❌ Lost', 'deleted': '🗑️ Deleted'}.get(d.get('status', ''), '❓')
print(f\"💼 Deal: {d.get('title', 'Untitled')}\")
print(f\"ID: {d.get('id')}\")
print(f\"Status: {status_icon}\")
print(f\"Value: {d.get('value', 0)} {d.get('currency', '')}\")

# Handle person - can be nested object or simple values
person_id = d.get('person_id')
if isinstance(person_id, dict):
    print(f\"Person: {person_id.get('name', '')} (ID: {person_id.get('value', '')})\")
elif d.get('person_name'):
    print(f\"Person: {d.get('person_name')} (ID: {person_id})\")

# Handle org - can be nested object or simple values  
org_id = d.get('org_id')
if isinstance(org_id, dict):
    print(f\"Organization: {org_id.get('name', '')} (ID: {org_id.get('value', '')})\")
elif d.get('org_name'):
    print(f\"Organization: {d.get('org_name')} (ID: {org_id})\")

print(f\"Pipeline: {d.get('pipeline_id')}\")
print(f\"Stage: {d.get('stage_id')}\")
if d.get('expected_close_date'): print(f\"Expected Close: {d.get('expected_close_date')}\")
if d.get('add_time'): print(f\"Created: {d.get('add_time')}\")
if d.get('won_time'): print(f\"Won: {d.get('won_time')}\")
if d.get('lost_time'): print(f\"Lost: {d.get('lost_time')}\")
if d.get('lost_reason'): print(f\"Lost Reason: {d.get('lost_reason')}\")
if d.get('probability'): print(f\"Probability: {d.get('probability')}%\")
print(f\"\\nActivities: {d.get('activities_count', 0)} total, {d.get('done_activities_count', 0)} done, {d.get('undone_activities_count', 0)} pending\")
print(f\"Notes: {d.get('notes_count', 0)}\")
print(f\"Files: {d.get('files_count', 0)}\")
"
}

# Show detailed person
show_person() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
p = data.get('data', {})
print(f\"👤 Person: {p.get('name', 'Unknown')}\")
print(f\"ID: {p.get('id')}\")
# Handle email array
emails = p.get('email') or []
if emails:
    for e in emails:
        if isinstance(e, dict):
            print(f\"Email ({e.get('label', 'work')}): {e.get('value', '')}\")
        else:
            print(f\"Email: {e}\")
# Handle phone array
phones = p.get('phone') or []
if phones:
    for ph in phones:
        if isinstance(ph, dict):
            print(f\"Phone ({ph.get('label', 'work')}): {ph.get('value', '')}\")
        else:
            print(f\"Phone: {ph}\")
# Organization
if p.get('org_id'):
    org = p.get('org_id')
    if isinstance(org, dict):
        print(f\"Organization: {org.get('name', '')} (ID: {org.get('value', '')})\")
    else:
        print(f\"Organization ID: {org}\")
if p.get('add_time'): print(f\"Created: {p.get('add_time')}\")
print(f\"\\nOpen deals: {p.get('open_deals_count', 0)}\")
print(f\"Closed deals: {p.get('closed_deals_count', 0)}\")
print(f\"Activities: {p.get('activities_count', 0)}\")
print(f\"Notes: {p.get('notes_count', 0)}\")
"
}

# Show detailed organization
show_org() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
o = data.get('data', {})
print(f\"🏢 Organization: {o.get('name', 'Unknown')}\")
print(f\"ID: {o.get('id')}\")
if o.get('address'): print(f\"Address: {o.get('address')}\")
if o.get('address_country'): print(f\"Country: {o.get('address_country')}\")
if o.get('cc_email'): print(f\"CC Email: {o.get('cc_email')}\")
if o.get('add_time'): print(f\"Created: {o.get('add_time')}\")
print(f\"\\nPeople: {o.get('people_count', 0)}\")
print(f\"Open deals: {o.get('open_deals_count', 0)}\")
print(f\"Won deals: {o.get('won_deals_count', 0)}\")
print(f\"Lost deals: {o.get('lost_deals_count', 0)}\")
print(f\"Activities: {o.get('activities_count', 0)}\")
print(f\"Notes: {o.get('notes_count', 0)}\")
"
}

# Show detailed activity
show_activity() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
a = data.get('data', {})
done_icon = '✅ Done' if a.get('done') else '⏳ Pending'
print(f\"📅 Activity: {a.get('subject', 'No subject')}\")
print(f\"ID: {a.get('id')}\")
print(f\"Type: {a.get('type', '-')}\")
print(f\"Status: {done_icon}\")
print(f\"Due: {a.get('due_date', '-')} {a.get('due_time', '')}\")
if a.get('duration'): print(f\"Duration: {a.get('duration')}\")
if a.get('deal_id'): print(f\"Deal: {a.get('deal_title', '')} (ID: {a.get('deal_id')})\")
if a.get('person_id'): print(f\"Person: {a.get('person_name', '')} (ID: {a.get('person_id')})\")
if a.get('org_id'): print(f\"Organization: {a.get('org_name', '')} (ID: {a.get('org_id')})\")
if a.get('note'): print(f\"Note: {a.get('note')[:200]}\")
if a.get('location'): print(f\"Location: {a.get('location')}\")
"
}

# Show detailed lead
show_lead() {
  python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
l = data.get('data', {})
print(f\"💡 Lead: {l.get('title', 'Untitled')}\")
print(f\"ID: {l.get('id')}\")
# Value handling
value = l.get('value') or {}
if isinstance(value, dict):
    print(f\"Value: {value.get('amount', 0)} {value.get('currency', '')}\")
elif value:
    print(f\"Value: {value}\")
if l.get('person_id'): print(f\"Person ID: {l.get('person_id')}\")
if l.get('organization_id'): print(f\"Organization ID: {l.get('organization_id')}\")
if l.get('expected_close_date'): print(f\"Expected Close: {l.get('expected_close_date')}\")
if l.get('add_time'): print(f\"Created: {l.get('add_time')}\")
if l.get('source_name'): print(f\"Source: {l.get('source_name')}\")
"
}

# Main command router
RESOURCE="$1"
COMMAND="$2"
shift 2 2>/dev/null || true

case "$RESOURCE" in
  deals)
    case "$COMMAND" in
      list)
        LIMIT=50
        START=0
        STATUS=""
        STAGE_ID=""
        USER_ID=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --limit) LIMIT="$2"; shift 2 ;;
            --start|--offset) START="$2"; shift 2 ;;
            --status) STATUS="$2"; shift 2 ;;
            --stage) STAGE_ID="$2"; shift 2 ;;
            --user) USER_ID="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        echo "💼 Listing deals..."
        QUERY="limit=$LIMIT&start=$START"
        [ -n "$STATUS" ] && QUERY="$QUERY&status=$STATUS"
        [ -n "$STAGE_ID" ] && QUERY="$QUERY&stage_id=$STAGE_ID"
        [ -n "$USER_ID" ] && QUERY="$QUERY&user_id=$USER_ID"
        pipedrive_api GET "/deals?$QUERY" | format_deals
        ;;
      
      search)
        QUERY="$1"
        if [ -z "$QUERY" ]; then
          echo "Usage: pipedrive.sh deals search \"query\""
          exit 1
        fi
        echo "🔍 Searching deals for: $QUERY"
        pipedrive_api GET "/itemSearch?term=$(echo "$QUERY" | python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read().strip()))')&item_types=deal&limit=50" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
items = data.get('data', {}).get('items', [])
if not items:
    print('No deals found.')
    sys.exit(0)
for item in items:
    d = item.get('item', {})
    print(f\"💼 {d.get('id')}\t{d.get('title', 'Untitled')[:40]}\t{d.get('value', 0)} {d.get('currency', '')}\t{d.get('person', {}).get('name', '')[:20] if d.get('person') else ''}\")
"
        ;;
      
      show)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh deals show <id>"
          exit 1
        fi
        pipedrive_api GET "/deals/$ID" | show_deal
        ;;
      
      create)
        TITLE=""
        PERSON_ID=""
        ORG_ID=""
        VALUE=""
        CURRENCY="USD"
        STAGE_ID=""
        PIPELINE_ID=""
        EXPECTED_CLOSE=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --title) TITLE="$2"; shift 2 ;;
            --person) PERSON_ID="$2"; shift 2 ;;
            --org) ORG_ID="$2"; shift 2 ;;
            --value) VALUE="$2"; shift 2 ;;
            --currency) CURRENCY="$2"; shift 2 ;;
            --stage) STAGE_ID="$2"; shift 2 ;;
            --pipeline) PIPELINE_ID="$2"; shift 2 ;;
            --expected-close) EXPECTED_CLOSE="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        
        if [ -z "$TITLE" ]; then
          echo "Usage: pipedrive.sh deals create --title \"Deal Title\" [--person <id>] [--org <id>] [--value N] [--currency USD] [--stage <id>] [--pipeline <id>]"
          exit 1
        fi
        
        echo "📝 Creating deal: $TITLE"
        DATA=$(python3 -c "
import json
data = {'title': '$TITLE'}
if '$PERSON_ID': data['person_id'] = int('$PERSON_ID')
if '$ORG_ID': data['org_id'] = int('$ORG_ID')
if '$VALUE': data['value'] = '$VALUE'
if '$CURRENCY': data['currency'] = '$CURRENCY'
if '$STAGE_ID': data['stage_id'] = int('$STAGE_ID')
if '$PIPELINE_ID': data['pipeline_id'] = int('$PIPELINE_ID')
if '$EXPECTED_CLOSE': data['expected_close_date'] = '$EXPECTED_CLOSE'
print(json.dumps(data))
")
        pipedrive_api POST "/deals" "$DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
d = data.get('data', {})
print(f\"✅ Created deal ID: {d.get('id')} - {d.get('title')}\")
"
        ;;
      
      update)
        ID="$1"
        shift
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh deals update <id> [--title x] [--value N] [--stage <id>] [--person <id>] [--org <id>]"
          exit 1
        fi
        
        TITLE=""
        PERSON_ID=""
        ORG_ID=""
        VALUE=""
        STAGE_ID=""
        STATUS=""
        EXPECTED_CLOSE=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --title) TITLE="$2"; shift 2 ;;
            --person) PERSON_ID="$2"; shift 2 ;;
            --org) ORG_ID="$2"; shift 2 ;;
            --value) VALUE="$2"; shift 2 ;;
            --stage) STAGE_ID="$2"; shift 2 ;;
            --status) STATUS="$2"; shift 2 ;;
            --expected-close) EXPECTED_CLOSE="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        
        echo "✏️ Updating deal $ID..."
        DATA=$(python3 -c "
import json
data = {}
if '$TITLE': data['title'] = '$TITLE'
if '$PERSON_ID': data['person_id'] = int('$PERSON_ID')
if '$ORG_ID': data['org_id'] = int('$ORG_ID')
if '$VALUE': data['value'] = '$VALUE'
if '$STAGE_ID': data['stage_id'] = int('$STAGE_ID')
if '$STATUS': data['status'] = '$STATUS'
if '$EXPECTED_CLOSE': data['expected_close_date'] = '$EXPECTED_CLOSE'
print(json.dumps(data))
")
        pipedrive_api PUT "/deals/$ID" "$DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
d = data.get('data', {})
print(f\"✅ Updated deal ID: {d.get('id')}\")
"
        ;;
      
      won)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh deals won <id>"
          exit 1
        fi
        echo "✅ Marking deal $ID as won..."
        pipedrive_api PUT "/deals/$ID" '{"status": "won"}' | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
print(f\"✅ Deal marked as won!\")
"
        ;;
      
      lost)
        ID="$1"
        shift
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh deals lost <id> [--reason \"Reason\"]"
          exit 1
        fi
        REASON=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --reason) REASON="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        echo "❌ Marking deal $ID as lost..."
        DATA=$(python3 -c "
import json
data = {'status': 'lost'}
if '$REASON': data['lost_reason'] = '$REASON'
print(json.dumps(data))
")
        pipedrive_api PUT "/deals/$ID" "$DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
print(f\"✅ Deal marked as lost!\")
"
        ;;
      
      delete)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh deals delete <id>"
          exit 1
        fi
        echo "🗑️ Deleting deal $ID..."
        pipedrive_api DELETE "/deals/$ID" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
print(f\"✅ Deal deleted!\")
"
        ;;
      
      *)
        echo "Deals commands: list, search, show, create, update, won, lost, delete"
        ;;
    esac
    ;;

  persons)
    case "$COMMAND" in
      list)
        LIMIT=50
        START=0
        while [ $# -gt 0 ]; do
          case "$1" in
            --limit) LIMIT="$2"; shift 2 ;;
            --start|--offset) START="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        echo "👤 Listing persons..."
        pipedrive_api GET "/persons?limit=$LIMIT&start=$START" | format_persons
        ;;
      
      search)
        QUERY="$1"
        if [ -z "$QUERY" ]; then
          echo "Usage: pipedrive.sh persons search \"query\""
          exit 1
        fi
        echo "🔍 Searching persons for: $QUERY"
        pipedrive_api GET "/itemSearch?term=$(echo "$QUERY" | python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read().strip()))')&item_types=person&limit=50" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
items = data.get('data', {}).get('items', [])
if not items:
    print('No persons found.')
    sys.exit(0)
for item in items:
    p = item.get('item', {})
    email = ''
    for e in p.get('emails', []):
        email = e
        break
    org = p.get('organization', {}).get('name', '') if p.get('organization') else ''
    print(f\"👤 {p.get('id')}\t{p.get('name', 'Unknown')[:35]}\t{email[:30]}\t{org[:25]}\")
"
        ;;
      
      show)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh persons show <id>"
          exit 1
        fi
        pipedrive_api GET "/persons/$ID" | show_person
        ;;
      
      create)
        NAME=""
        EMAIL=""
        PHONE=""
        ORG_ID=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --name) NAME="$2"; shift 2 ;;
            --email) EMAIL="$2"; shift 2 ;;
            --phone) PHONE="$2"; shift 2 ;;
            --org) ORG_ID="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        
        if [ -z "$NAME" ]; then
          echo "Usage: pipedrive.sh persons create --name \"Name\" [--email x] [--phone x] [--org <id>]"
          exit 1
        fi
        
        echo "📝 Creating person: $NAME"
        DATA=$(python3 -c "
import json
data = {'name': '$NAME'}
if '$EMAIL': data['email'] = [{'value': '$EMAIL', 'primary': True, 'label': 'work'}]
if '$PHONE': data['phone'] = [{'value': '$PHONE', 'primary': True, 'label': 'work'}]
if '$ORG_ID': data['org_id'] = int('$ORG_ID')
print(json.dumps(data))
")
        pipedrive_api POST "/persons" "$DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
p = data.get('data', {})
print(f\"✅ Created person ID: {p.get('id')} - {p.get('name')}\")
"
        ;;
      
      update)
        ID="$1"
        shift
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh persons update <id> [--name x] [--email x] [--phone x] [--org <id>]"
          exit 1
        fi
        
        NAME=""
        EMAIL=""
        PHONE=""
        ORG_ID=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --name) NAME="$2"; shift 2 ;;
            --email) EMAIL="$2"; shift 2 ;;
            --phone) PHONE="$2"; shift 2 ;;
            --org) ORG_ID="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        
        echo "✏️ Updating person $ID..."
        DATA=$(python3 -c "
import json
data = {}
if '$NAME': data['name'] = '$NAME'
if '$EMAIL': data['email'] = [{'value': '$EMAIL', 'primary': True, 'label': 'work'}]
if '$PHONE': data['phone'] = [{'value': '$PHONE', 'primary': True, 'label': 'work'}]
if '$ORG_ID': data['org_id'] = int('$ORG_ID')
print(json.dumps(data))
")
        pipedrive_api PUT "/persons/$ID" "$DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
p = data.get('data', {})
print(f\"✅ Updated person ID: {p.get('id')}\")
"
        ;;
      
      delete)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh persons delete <id>"
          exit 1
        fi
        echo "🗑️ Deleting person $ID..."
        pipedrive_api DELETE "/persons/$ID" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
print(f\"✅ Person deleted!\")
"
        ;;
      
      *)
        echo "Persons commands: list, search, show, create, update, delete"
        ;;
    esac
    ;;

  orgs|organizations)
    case "$COMMAND" in
      list)
        LIMIT=50
        START=0
        while [ $# -gt 0 ]; do
          case "$1" in
            --limit) LIMIT="$2"; shift 2 ;;
            --start|--offset) START="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        echo "🏢 Listing organizations..."
        pipedrive_api GET "/organizations?limit=$LIMIT&start=$START" | format_orgs
        ;;
      
      search)
        QUERY="$1"
        if [ -z "$QUERY" ]; then
          echo "Usage: pipedrive.sh orgs search \"query\""
          exit 1
        fi
        echo "🔍 Searching organizations for: $QUERY"
        pipedrive_api GET "/itemSearch?term=$(echo "$QUERY" | python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read().strip()))')&item_types=organization&limit=50" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
items = data.get('data', {}).get('items', [])
if not items:
    print('No organizations found.')
    sys.exit(0)
for item in items:
    o = item.get('item', {})
    print(f\"🏢 {o.get('id')}\t{o.get('name', 'Unknown')[:40]}\t{o.get('address', '')[:30]}\")
"
        ;;
      
      show)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh orgs show <id>"
          exit 1
        fi
        pipedrive_api GET "/organizations/$ID" | show_org
        ;;
      
      create)
        NAME=""
        ADDRESS=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --name) NAME="$2"; shift 2 ;;
            --address) ADDRESS="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        
        if [ -z "$NAME" ]; then
          echo "Usage: pipedrive.sh orgs create --name \"Org Name\" [--address \"Address\"]"
          exit 1
        fi
        
        echo "📝 Creating organization: $NAME"
        DATA=$(python3 -c "
import json
data = {'name': '$NAME'}
if '$ADDRESS': data['address'] = '$ADDRESS'
print(json.dumps(data))
")
        pipedrive_api POST "/organizations" "$DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
o = data.get('data', {})
print(f\"✅ Created organization ID: {o.get('id')} - {o.get('name')}\")
"
        ;;
      
      update)
        ID="$1"
        shift
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh orgs update <id> [--name x] [--address x]"
          exit 1
        fi
        
        NAME=""
        ADDRESS=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --name) NAME="$2"; shift 2 ;;
            --address) ADDRESS="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        
        echo "✏️ Updating organization $ID..."
        DATA=$(python3 -c "
import json
data = {}
if '$NAME': data['name'] = '$NAME'
if '$ADDRESS': data['address'] = '$ADDRESS'
print(json.dumps(data))
")
        pipedrive_api PUT "/organizations/$ID" "$DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
o = data.get('data', {})
print(f\"✅ Updated organization ID: {o.get('id')}\")
"
        ;;
      
      delete)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh orgs delete <id>"
          exit 1
        fi
        echo "🗑️ Deleting organization $ID..."
        pipedrive_api DELETE "/organizations/$ID" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
print(f\"✅ Organization deleted!\")
"
        ;;
      
      *)
        echo "Organizations commands: list, search, show, create, update, delete"
        ;;
    esac
    ;;

  activities)
    case "$COMMAND" in
      list)
        LIMIT=50
        START=0
        DONE=""
        DEAL_ID=""
        USER_ID=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --limit) LIMIT="$2"; shift 2 ;;
            --start|--offset) START="$2"; shift 2 ;;
            --done) DONE="$2"; shift 2 ;;
            --deal) DEAL_ID="$2"; shift 2 ;;
            --user) USER_ID="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        echo "📅 Listing activities..."
        QUERY="limit=$LIMIT&start=$START"
        [ -n "$DONE" ] && QUERY="$QUERY&done=$DONE"
        [ -n "$DEAL_ID" ] && QUERY="$QUERY&deal_id=$DEAL_ID"
        [ -n "$USER_ID" ] && QUERY="$QUERY&user_id=$USER_ID"
        pipedrive_api GET "/activities?$QUERY" | format_activities
        ;;
      
      show)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh activities show <id>"
          exit 1
        fi
        pipedrive_api GET "/activities/$ID" | show_activity
        ;;
      
      create)
        SUBJECT=""
        TYPE="task"
        DEAL_ID=""
        PERSON_ID=""
        ORG_ID=""
        DUE_DATE=""
        DUE_TIME=""
        DURATION=""
        NOTE=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --subject) SUBJECT="$2"; shift 2 ;;
            --type) TYPE="$2"; shift 2 ;;
            --deal) DEAL_ID="$2"; shift 2 ;;
            --person) PERSON_ID="$2"; shift 2 ;;
            --org) ORG_ID="$2"; shift 2 ;;
            --date) DUE_DATE="$2"; shift 2 ;;
            --time) DUE_TIME="$2"; shift 2 ;;
            --duration) DURATION="$2"; shift 2 ;;
            --note) NOTE="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        
        if [ -z "$SUBJECT" ]; then
          echo "Usage: pipedrive.sh activities create --subject \"Subject\" [--type call|meeting|task] [--deal <id>] [--person <id>] [--date YYYY-MM-DD] [--time HH:MM]"
          exit 1
        fi
        
        echo "📝 Creating activity: $SUBJECT"
        DATA=$(python3 -c "
import json
from datetime import date
data = {
    'subject': '$SUBJECT',
    'type': '$TYPE',
    'due_date': '${DUE_DATE:-$(date +%Y-%m-%d)}'
}
if '$DEAL_ID': data['deal_id'] = int('$DEAL_ID')
if '$PERSON_ID': data['person_id'] = int('$PERSON_ID')
if '$ORG_ID': data['org_id'] = int('$ORG_ID')
if '$DUE_TIME': data['due_time'] = '$DUE_TIME'
if '$DURATION': data['duration'] = '$DURATION'
if '$NOTE': data['note'] = '$NOTE'
print(json.dumps(data))
")
        pipedrive_api POST "/activities" "$DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
a = data.get('data', {})
print(f\"✅ Created activity ID: {a.get('id')} - {a.get('subject')}\")
"
        ;;
      
      done)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh activities done <id>"
          exit 1
        fi
        echo "✅ Marking activity $ID as done..."
        pipedrive_api PUT "/activities/$ID" '{"done": true}' | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
print(f\"✅ Activity marked as done!\")
"
        ;;
      
      *)
        echo "Activities commands: list, show, create, done"
        ;;
    esac
    ;;

  pipelines)
    case "$COMMAND" in
      list)
        echo "📊 Listing pipelines..."
        pipedrive_api GET "/pipelines" | format_pipelines
        ;;
      
      stages)
        PIPELINE_ID="$1"
        if [ -z "$PIPELINE_ID" ]; then
          echo "Usage: pipedrive.sh pipelines stages <pipeline_id>"
          exit 1
        fi
        echo "📊 Stages for pipeline $PIPELINE_ID:"
        pipedrive_api GET "/stages?pipeline_id=$PIPELINE_ID" | format_stages
        ;;
      
      *)
        echo "Pipelines commands: list, stages <pipeline_id>"
        ;;
    esac
    ;;

  leads)
    case "$COMMAND" in
      list)
        LIMIT=50
        START=0
        while [ $# -gt 0 ]; do
          case "$1" in
            --limit) LIMIT="$2"; shift 2 ;;
            --start|--offset) START="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        echo "💡 Listing leads..."
        pipedrive_api GET "/leads?limit=$LIMIT&start=$START" | format_leads
        ;;
      
      show)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh leads show <id>"
          exit 1
        fi
        pipedrive_api GET "/leads/$ID" | show_lead
        ;;
      
      create)
        TITLE=""
        PERSON_ID=""
        ORG_ID=""
        VALUE=""
        CURRENCY="USD"
        EXPECTED_CLOSE=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --title) TITLE="$2"; shift 2 ;;
            --person) PERSON_ID="$2"; shift 2 ;;
            --org) ORG_ID="$2"; shift 2 ;;
            --value) VALUE="$2"; shift 2 ;;
            --currency) CURRENCY="$2"; shift 2 ;;
            --expected-close) EXPECTED_CLOSE="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        
        if [ -z "$TITLE" ]; then
          echo "Usage: pipedrive.sh leads create --title \"Lead Title\" [--person <id>] [--org <id>] [--value N] [--currency USD]"
          exit 1
        fi
        
        echo "📝 Creating lead: $TITLE"
        DATA=$(python3 -c "
import json
data = {'title': '$TITLE'}
if '$PERSON_ID': data['person_id'] = '$PERSON_ID'
if '$ORG_ID': data['organization_id'] = '$ORG_ID'
if '$VALUE': data['value'] = {'amount': float('$VALUE'), 'currency': '$CURRENCY'}
if '$EXPECTED_CLOSE': data['expected_close_date'] = '$EXPECTED_CLOSE'
print(json.dumps(data))
")
        pipedrive_api POST "/leads" "$DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
l = data.get('data', {})
print(f\"✅ Created lead ID: {l.get('id')} - {l.get('title')}\")
"
        ;;
      
      convert)
        ID="$1"
        if [ -z "$ID" ]; then
          echo "Usage: pipedrive.sh leads convert <id>"
          exit 1
        fi
        echo "🔄 Converting lead $ID to deal..."
        # First get the lead details
        LEAD_DATA=$(pipedrive_api GET "/leads/$ID")
        
        # Create deal from lead
        python3 -c "
import json
import subprocess
import sys

lead_resp = json.loads('''$LEAD_DATA''')
if not lead_resp.get('success'):
    print(f\"❌ Error getting lead: {lead_resp.get('error', 'Unknown error')}\")
    sys.exit(1)

lead = lead_resp.get('data', {})
deal_data = {
    'title': lead.get('title', 'Converted Lead')
}

if lead.get('person_id'):
    deal_data['person_id'] = lead['person_id']
if lead.get('organization_id'):
    deal_data['org_id'] = lead['organization_id']

value = lead.get('value')
if value and isinstance(value, dict):
    deal_data['value'] = value.get('amount', 0)
    deal_data['currency'] = value.get('currency', 'USD')

print(json.dumps(deal_data))
" > /tmp/lead_convert_data.json 2>/dev/null || exit 1
        
        DEAL_RESULT=$(pipedrive_api POST "/deals" "$(cat /tmp/lead_convert_data.json)")
        rm -f /tmp/lead_convert_data.json
        
        echo "$DEAL_RESULT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
d = data.get('data', {})
print(f\"✅ Created deal ID: {d.get('id')} from lead\")
print(f\"Note: Original lead still exists. Delete it manually if needed.\")
"
        ;;
      
      *)
        echo "Leads commands: list, show, create, convert"
        ;;
    esac
    ;;

  products)
    case "$COMMAND" in
      list)
        LIMIT=50
        START=0
        while [ $# -gt 0 ]; do
          case "$1" in
            --limit) LIMIT="$2"; shift 2 ;;
            --start|--offset) START="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        echo "📦 Listing products..."
        pipedrive_api GET "/products?limit=$LIMIT&start=$START" | format_products
        ;;
      
      search)
        QUERY="$1"
        if [ -z "$QUERY" ]; then
          echo "Usage: pipedrive.sh products search \"query\""
          exit 1
        fi
        echo "🔍 Searching products for: $QUERY"
        pipedrive_api GET "/itemSearch?term=$(echo "$QUERY" | python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read().strip()))')&item_types=product&limit=50" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
items = data.get('data', {}).get('items', [])
if not items:
    print('No products found.')
    sys.exit(0)
for item in items:
    p = item.get('item', {})
    print(f\"📦 {p.get('id')}\t{p.get('name', 'Unknown')[:40]}\t{p.get('code', '')[:15]}\")
"
        ;;
      
      *)
        echo "Products commands: list, search"
        ;;
    esac
    ;;

  notes)
    case "$COMMAND" in
      list)
        LIMIT=50
        START=0
        DEAL_ID=""
        PERSON_ID=""
        ORG_ID=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --limit) LIMIT="$2"; shift 2 ;;
            --start|--offset) START="$2"; shift 2 ;;
            --deal) DEAL_ID="$2"; shift 2 ;;
            --person) PERSON_ID="$2"; shift 2 ;;
            --org) ORG_ID="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        echo "📝 Listing notes..."
        QUERY="limit=$LIMIT&start=$START"
        [ -n "$DEAL_ID" ] && QUERY="$QUERY&deal_id=$DEAL_ID"
        [ -n "$PERSON_ID" ] && QUERY="$QUERY&person_id=$PERSON_ID"
        [ -n "$ORG_ID" ] && QUERY="$QUERY&org_id=$ORG_ID"
        pipedrive_api GET "/notes?$QUERY" | format_notes
        ;;
      
      create)
        CONTENT=""
        DEAL_ID=""
        PERSON_ID=""
        ORG_ID=""
        PINNED=""
        while [ $# -gt 0 ]; do
          case "$1" in
            --content) CONTENT="$2"; shift 2 ;;
            --deal) DEAL_ID="$2"; shift 2 ;;
            --person) PERSON_ID="$2"; shift 2 ;;
            --org) ORG_ID="$2"; shift 2 ;;
            --pinned) PINNED="true"; shift ;;
            *) shift ;;
          esac
        done
        
        if [ -z "$CONTENT" ]; then
          echo "Usage: pipedrive.sh notes create --content \"Note text\" [--deal <id>] [--person <id>] [--org <id>] [--pinned]"
          exit 1
        fi
        
        if [ -z "$DEAL_ID" ] && [ -z "$PERSON_ID" ] && [ -z "$ORG_ID" ]; then
          echo "Error: Must specify at least one of --deal, --person, or --org"
          exit 1
        fi
        
        echo "📝 Creating note..."
        DATA=$(python3 -c "
import json
data = {'content': '''$CONTENT'''}
if '$DEAL_ID': 
    data['deal_id'] = int('$DEAL_ID')
    if '$PINNED': data['pinned_to_deal_flag'] = 1
if '$PERSON_ID': 
    data['person_id'] = int('$PERSON_ID')
    if '$PINNED': data['pinned_to_person_flag'] = 1
if '$ORG_ID': 
    data['org_id'] = int('$ORG_ID')
    if '$PINNED': data['pinned_to_organization_flag'] = 1
print(json.dumps(data))
")
        pipedrive_api POST "/notes" "$DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data.get('success'):
    print(f\"❌ Error: {data.get('error', 'Unknown error')}\")
    sys.exit(1)
n = data.get('data', {})
print(f\"✅ Created note ID: {n.get('id')}\")
"
        ;;
      
      *)
        echo "Notes commands: list, create"
        ;;
    esac
    ;;

  *)
    echo "Pipedrive CRM CLI"
    echo ""
    echo "Resources:"
    echo "  deals       Manage deals (list, search, show, create, update, won, lost, delete)"
    echo "  persons     Manage contacts (list, search, show, create, update, delete)"
    echo "  orgs        Manage organizations (list, search, show, create, update, delete)"
    echo "  activities  Manage activities (list, show, create, done)"
    echo "  pipelines   View pipelines and stages (list, stages)"
    echo "  leads       Manage leads (list, show, create, convert)"
    echo "  products    View products (list, search)"
    echo "  notes       Manage notes (list, create)"
    echo ""
    echo "Usage: pipedrive.sh <resource> <command> [options]"
    echo ""
    echo "Examples:"
    echo "  pipedrive.sh deals list"
    echo "  pipedrive.sh deals search \"Acme\""
    echo "  pipedrive.sh persons create --name \"John Doe\" --email \"john@example.com\""
    ;;
esac
