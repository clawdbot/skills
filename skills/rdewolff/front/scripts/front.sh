#!/bin/bash
# Front.app API CLI
# Usage: front.sh <command> [args...]

set -e

# Get API token from env or clawdbot config
if [ -z "$FRONT_API_TOKEN" ]; then
  FRONT_API_TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.clawdbot/clawdbot.json'))['skills']['entries']['front']['apiKey'])" 2>/dev/null || echo "")
fi

if [ -z "$FRONT_API_TOKEN" ]; then
  echo "Error: FRONT_API_TOKEN not set. Configure in ~/.clawdbot/clawdbot.json or set env var."
  exit 1
fi

# Use company-specific API subdomain (auto-detected from inboxes call)
API_BASE="https://api2.frontapp.com"
# Try to get company subdomain from a quick call
COMPANY_BASE=$(curl -s "$API_BASE/inboxes" -H "Authorization: Bearer $FRONT_API_TOKEN" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('_links',{}).get('self','').split('/')[2])" 2>/dev/null || echo "")
if [ -n "$COMPANY_BASE" ] && [ "$COMPANY_BASE" != "api2.frontapp.com" ]; then
  API_BASE="https://$COMPANY_BASE"
fi

# Helper function for API calls
front_api() {
  local method="$1"
  local endpoint="$2"
  local data="$3"
  
  if [ -n "$data" ]; then
    curl -s -X "$method" "$API_BASE$endpoint" \
      -H "Authorization: Bearer $FRONT_API_TOKEN" \
      -H "Content-Type: application/json" \
      -d "$data"
  else
    curl -s -X "$method" "$API_BASE$endpoint" \
      -H "Authorization: Bearer $FRONT_API_TOKEN" \
      -H "Content-Type: application/json"
  fi
}

# Commands
case "$1" in
  inboxes)
    echo "📥 Listing inboxes..."
    front_api GET "/inboxes" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for inbox in data.get('_results', []):
    print(f\"{inbox['id']}\t{inbox['name']}\t{inbox.get('address', 'N/A')}\")
" 2>/dev/null || front_api GET "/inboxes"
    ;;
    
  conversations)
    shift
    INBOX_ID=""
    STATUS=""  # Default to non-archived statuses
    INCLUDE_ARCHIVED=""
    UNASSIGNED_ONLY=""
    ASSIGNED_ONLY=""
    LIMIT="100"
    while [ $# -gt 0 ]; do
      case "$1" in
        --status) STATUS="$2"; shift 2 ;;
        --all) INCLUDE_ARCHIVED="true"; shift ;;
        --archived) STATUS="archived"; shift ;;
        --unassigned) UNASSIGNED_ONLY="true"; shift ;;
        --assigned) ASSIGNED_ONLY="true"; shift ;;
        --limit) LIMIT="$2"; shift 2 ;;
        *) INBOX_ID="$1"; shift ;;
      esac
    done
    
    ENDPOINT="/conversations"
    if [ -n "$INBOX_ID" ]; then
      ENDPOINT="/inboxes/$INBOX_ID/conversations"
    fi
    
    # Build query params - use API-level filtering for efficiency
    # URL-encode brackets: [ = %5B, ] = %5D
    PARAMS="?limit=$LIMIT"
    if [ -n "$STATUS" ]; then
      # Single explicit status
      PARAMS="$PARAMS&q%5Bstatuses%5D%5B%5D=$STATUS"
    elif [ -z "$INCLUDE_ARCHIVED" ]; then
      # Default: fetch unassigned + assigned (skip archived/deleted)
      PARAMS="$PARAMS&q%5Bstatuses%5D%5B%5D=unassigned&q%5Bstatuses%5D%5B%5D=assigned"
    fi
    
    echo "💬 Listing conversations..."
    front_api GET "$ENDPOINT$PARAMS" | python3 -c "
import json, sys
data = json.load(sys.stdin)
results = data.get('_results', [])
unassigned_only = '$UNASSIGNED_ONLY' == 'true'
assigned_only = '$ASSIGNED_ONLY' == 'true'
if unassigned_only:
    results = [c for c in results if c.get('status') == 'unassigned']
if assigned_only:
    results = [c for c in results if c.get('status') == 'assigned']
print(f'Found {len(results)} conversations')
for c in results[:50]:
    subject = c.get('subject', 'No subject')[:50]
    status = c.get('status', 'unknown')
    assignee = c.get('assignee', {}).get('email', 'unassigned') if c.get('assignee') else 'unassigned'
    print(f\"{c['id']}\t[{status}]\t{assignee}\t{subject}\")
" 2>/dev/null || front_api GET "$ENDPOINT$PARAMS"
    ;;
    
  conversation)
    CONV_ID="$2"
    if [ -z "$CONV_ID" ]; then
      echo "Usage: front.sh conversation <conversation_id>"
      exit 1
    fi
    echo "📧 Getting conversation $CONV_ID..."
    front_api GET "/conversations/$CONV_ID"
    ;;
    
  messages)
    CONV_ID="$2"
    if [ -z "$CONV_ID" ]; then
      echo "Usage: front.sh messages <conversation_id>"
      exit 1
    fi
    echo "📨 Messages in $CONV_ID..."
    front_api GET "/conversations/$CONV_ID/messages" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for m in data.get('_results', []):
    sender = m.get('author', {}).get('email', 'unknown') if m.get('author') else m.get('recipients', [{}])[0].get('handle', 'unknown')
    body = m.get('body', '')[:200].replace('\n', ' ')
    print(f\"---\nFrom: {sender}\nType: {m.get('type', 'unknown')}\n{body}\n\")
" 2>/dev/null || front_api GET "/conversations/$CONV_ID/messages"
    ;;
    
  search)
    QUERY="$2"
    if [ -z "$QUERY" ]; then
      echo "Usage: front.sh search \"query\""
      exit 1
    fi
    echo "🔍 Searching for: $QUERY"
    front_api POST "/conversations/search" "{\"query\": \"$QUERY\"}" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for c in data.get('_results', [])[:20]:
    subject = c.get('subject', 'No subject')[:50]
    status = c.get('status', 'unknown')
    print(f\"{c['id']}\t[{status}]\t{subject}\")
" 2>/dev/null || front_api POST "/conversations/search" "{\"query\": \"$QUERY\"}"
    ;;
    
  comments)
    CONV_ID="$2"
    if [ -z "$CONV_ID" ]; then
      echo "Usage: front.sh comments <conversation_id>"
      exit 1
    fi
    echo "💭 Comments on $CONV_ID..."
    front_api GET "/conversations/$CONV_ID/comments" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for c in data.get('_results', []):
    author = c.get('author', {}).get('email', 'unknown')
    body = c.get('body', '')
    print(f\"---\n👤 {author}:\n{body}\n\")
" 2>/dev/null || front_api GET "/conversations/$CONV_ID/comments"
    ;;
    
  add-comment)
    CONV_ID="$2"
    BODY="$3"
    if [ -z "$CONV_ID" ] || [ -z "$BODY" ]; then
      echo "Usage: front.sh add-comment <conversation_id> \"comment text\""
      exit 1
    fi
    echo "💬 Adding comment to $CONV_ID..."
    front_api POST "/conversations/$CONV_ID/comments" "{\"body\": \"$BODY\"}"
    echo "✅ Comment added!"
    ;;
    
  reply)
    CONV_ID="$2"
    BODY="$3"
    DRAFT=""
    if [ "$4" = "--draft" ]; then
      DRAFT="true"
    fi
    if [ -z "$CONV_ID" ] || [ -z "$BODY" ]; then
      echo "Usage: front.sh reply <conversation_id> \"message\" [--draft]"
      exit 1
    fi
    
    if [ -n "$DRAFT" ]; then
      echo "📝 Creating draft in $CONV_ID..."
      front_api POST "/conversations/$CONV_ID/drafts" "{\"body\": \"$BODY\"}"
      echo "✅ Draft saved!"
    else
      echo "📤 Sending reply to $CONV_ID..."
      front_api POST "/conversations/$CONV_ID/messages" "{\"body\": \"$BODY\"}"
      echo "✅ Reply sent!"
    fi
    ;;
    
  teammates)
    echo "👥 Listing teammates..."
    front_api GET "/teammates" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for t in data.get('_results', []):
    print(f\"{t['id']}\t{t['email']}\t{t.get('first_name', '')} {t.get('last_name', '')}\")
" 2>/dev/null || front_api GET "/teammates"
    ;;
    
  assign)
    CONV_ID="$2"
    TEAMMATE_ID="$3"
    if [ -z "$CONV_ID" ] || [ -z "$TEAMMATE_ID" ]; then
      echo "Usage: front.sh assign <conversation_id> <teammate_id>"
      exit 1
    fi
    echo "👤 Assigning $CONV_ID to $TEAMMATE_ID..."
    front_api PUT "/conversations/$CONV_ID/assignee" "{\"assignee_id\": \"$TEAMMATE_ID\"}"
    echo "✅ Assigned!"
    ;;
    
  tags)
    echo "🏷️ Listing tags..."
    front_api GET "/tags" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for t in data.get('_results', []):
    print(f\"{t['id']}\t{t['name']}\")
" 2>/dev/null || front_api GET "/tags"
    ;;
    
  tag)
    CONV_ID="$2"
    TAG_ID="$3"
    if [ -z "$CONV_ID" ] || [ -z "$TAG_ID" ]; then
      echo "Usage: front.sh tag <conversation_id> <tag_id>"
      exit 1
    fi
    echo "🏷️ Tagging $CONV_ID with $TAG_ID..."
    front_api POST "/conversations/$CONV_ID/tags" "{\"tag_ids\": [\"$TAG_ID\"]}"
    echo "✅ Tagged!"
    ;;
    
  contact)
    CONTACT="$2"
    if [ -z "$CONTACT" ]; then
      echo "Usage: front.sh contact <contact_id_or_handle>"
      exit 1
    fi
    echo "👤 Getting contact $CONTACT..."
    # Try as ID first, then as handle
    front_api GET "/contacts/$CONTACT" 2>/dev/null || front_api GET "/contacts/alt:email:$CONTACT"
    ;;
    
  drafts)
    INBOX_ID="$2"
    echo "📝 Looking for drafts..."
    # Get conversations and check each for drafts
    if [ -n "$INBOX_ID" ]; then
      ENDPOINT="/inboxes/$INBOX_ID/conversations?limit=50"
    else
      ENDPOINT="/conversations?limit=100"
    fi
    # Get conversation IDs then check each for drafts
    CONV_IDS=$(front_api GET "$ENDPOINT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for c in data.get('_results', []):
    if c.get('status') not in ('archived', 'deleted'):
        print(c['id'])
" 2>/dev/null)
    
    FOUND=0
    for cnv in $CONV_IDS; do
      DRAFTS=$(front_api GET "/conversations/$cnv/drafts" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for d in data.get('_results', []):
    print(f\"$cnv\t{d.get('id','?')}\t{d.get('subject', 'No subject')[:50]}\")
" 2>/dev/null)
      if [ -n "$DRAFTS" ]; then
        echo "$DRAFTS"
        FOUND=$((FOUND + 1))
      fi
    done
    
    if [ "$FOUND" -eq 0 ]; then
      echo "No drafts found in active conversations."
      echo "Note: Front API doesn't have a global drafts endpoint."
      echo "Drafts are stored per-conversation and require checking each one."
    fi
    ;;
    
  *)
    echo "Front.app CLI"
    echo ""
    echo "Commands:"
    echo "  inboxes                           List all inboxes"
    echo "  conversations [inbox_id]          List conversations (optionally from specific inbox)"
    echo "    --status open|archived|deleted  Filter by status"
    echo "    --unassigned                    Show only unassigned"
    echo "  conversation <id>                 Get conversation details"
    echo "  messages <conversation_id>        List messages in conversation"
    echo "  search \"query\"                    Search conversations"
    echo "  comments <conversation_id>        List team comments"
    echo "  add-comment <id> \"text\"           Add team comment"
    echo "  reply <id> \"message\" [--draft]    Reply to conversation (or save draft)"
    echo "  teammates                         List team members"
    echo "  assign <conv_id> <teammate_id>    Assign conversation"
    echo "  tags                              List available tags"
    echo "  tag <conv_id> <tag_id>            Add tag to conversation"
    echo "  contact <id_or_email>             Get contact info"
    ;;
esac
