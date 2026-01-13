#!/bin/bash
# Shared Memory - Manage users, groups, and permissions
# Uses Ensue - a shared memory network for agents
#
# Usage: ./scripts/shared-memory.sh <action> [args...]
#
# Actions:
#   create-user <username>
#   delete-user <username>
#   create-group <group_name>
#   delete-group <group_name>
#   add-member <group_name> <username>
#   remove-member <group_name> <username>
#   grant <target_type> <target_name> <action> <key_pattern>
#   revoke <grant_id>
#   list [target_type] [action]
#   subscribe <key_name>
#   unsubscribe <key_name>
#   list-subscriptions

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Find Ensue API key from various sources
find_api_key() {
  if [ -n "${ENSUE_API_KEY:-}" ]; then
    echo "$ENSUE_API_KEY"
    return
  fi

  # Check learning-memory plugin
  local key_file="$HOME/.claude/plugins/cache/ensue-learning-memory/ensue-learning-memory/0.2.0/.ensue-key"
  if [ -f "$key_file" ]; then
    cat "$key_file"
    return
  fi

  # Check ensue-memory plugin
  key_file="$HOME/.claude/plugins/cache/ensue-memory-network/ensue-memory/0.1.0/.ensue-key"
  if [ -f "$key_file" ]; then
    cat "$key_file"
    return
  fi

  # Check clawdbot config
  if [ -f "$HOME/.clawdbot/clawdbot.json" ]; then
    local key=$(grep -A2 '"ensue-learning-memory"' "$HOME/.clawdbot/clawdbot.json" | grep '"apiKey"' | cut -d'"' -f4)
    if [ -n "$key" ]; then
      echo "$key"
      return
    fi
  fi

  echo ""
}

ENSUE_API_KEY=$(find_api_key)

if [ -z "$ENSUE_API_KEY" ]; then
  echo '{"error":"ENSUE_API_KEY not found. Get a free API key at https://www.ensue-network.ai/login then configure it in clawdbot.json under skills.entries.ensue-learning-memory.apiKey or set as ENSUE_API_KEY environment variable."}'
  exit 1
fi

call_api() {
  local method="$1"
  local args="$2"

  curl -s -X POST https://api.ensue-network.ai/ \
    -H "Authorization: Bearer $ENSUE_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"$method\",\"arguments\":$args},\"id\":1}" \
    | sed 's/^data: //'
}

ACTION="${1:-}"

case "$ACTION" in
  create-user)
    USERNAME="${2:?Username required}"
    call_api "share" "{\"command\":{\"command\":\"create_user\",\"username\":\"$USERNAME\"}}"
    ;;

  delete-user)
    USERNAME="${2:?Username required}"
    call_api "share" "{\"command\":{\"command\":\"delete_user\",\"username\":\"$USERNAME\"}}"
    ;;

  create-group)
    GROUP="${2:?Group name required}"
    call_api "share" "{\"command\":{\"command\":\"create_group\",\"group_name\":\"$GROUP\"}}"
    ;;

  delete-group)
    GROUP="${2:?Group name required}"
    call_api "share" "{\"command\":{\"command\":\"delete_group\",\"group_name\":\"$GROUP\"}}"
    ;;

  add-member)
    GROUP="${2:?Group name required}"
    USERNAME="${3:?Username required}"
    call_api "share" "{\"command\":{\"command\":\"add_member\",\"group_name\":\"$GROUP\",\"username\":\"$USERNAME\"}}"
    ;;

  remove-member)
    GROUP="${2:?Group name required}"
    USERNAME="${3:?Username required}"
    call_api "share" "{\"command\":{\"command\":\"remove_member\",\"group_name\":\"$GROUP\",\"username\":\"$USERNAME\"}}"
    ;;

  grant)
    TARGET_TYPE="${2:?Target type required (org|user|group)}"
    TARGET_NAME="${3:-}"
    GRANT_ACTION="${4:?Action required (read|create|update|delete)}"
    KEY_PATTERN="${5:?Key pattern required}"

    if [ "$TARGET_TYPE" = "org" ]; then
      call_api "share" "{\"command\":{\"command\":\"grant\",\"target\":{\"type\":\"org\"},\"action\":\"$GRANT_ACTION\",\"key_pattern\":\"$KEY_PATTERN\"}}"
    elif [ "$TARGET_TYPE" = "user" ]; then
      call_api "share" "{\"command\":{\"command\":\"grant\",\"target\":{\"type\":\"user\",\"username\":\"$TARGET_NAME\"},\"action\":\"$GRANT_ACTION\",\"key_pattern\":\"$KEY_PATTERN\"}}"
    elif [ "$TARGET_TYPE" = "group" ]; then
      call_api "share" "{\"command\":{\"command\":\"grant\",\"target\":{\"type\":\"group\",\"group_name\":\"$TARGET_NAME\"},\"action\":\"$GRANT_ACTION\",\"key_pattern\":\"$KEY_PATTERN\"}}"
    else
      echo '{"error":"Invalid target type. Use: org, user, or group"}'
      exit 1
    fi
    ;;

  revoke)
    GRANT_ID="${2:?Grant ID required}"
    call_api "share" "{\"command\":{\"command\":\"revoke\",\"grant_id\":\"$GRANT_ID\"}}"
    ;;

  list)
    TARGET_TYPE="${2:-}"
    LIST_ACTION="${3:-}"
    if [ -n "$TARGET_TYPE" ] && [ -n "$LIST_ACTION" ]; then
      call_api "share" "{\"command\":{\"command\":\"list\",\"target_type\":\"$TARGET_TYPE\",\"action\":\"$LIST_ACTION\"}}"
    elif [ -n "$TARGET_TYPE" ]; then
      call_api "share" "{\"command\":{\"command\":\"list\",\"target_type\":\"$TARGET_TYPE\"}}"
    else
      call_api "share" "{\"command\":{\"command\":\"list\"}}"
    fi
    ;;

  subscribe)
    KEY_NAME="${2:?Key name required}"
    call_api "subscribe_to_memory" "{\"key_name\":\"$KEY_NAME\"}"
    ;;

  unsubscribe)
    KEY_NAME="${2:?Key name required}"
    call_api "unsubscribe_from_memory" "{\"key_name\":\"$KEY_NAME\"}"
    ;;

  list-subscriptions)
    call_api "list_subscriptions" "{}"
    ;;

  list-permissions)
    call_api "list_permissions" "{}"
    ;;

  *)
    cat << 'EOF'
Shared Memory - Manage users, groups, and permissions
Uses Ensue - a shared memory network for agents

Usage: ./scripts/shared-memory.sh <action> [args...]

User Management:
  create-user <username>           Create a new user
  delete-user <username>           Delete a user

Group Management:
  create-group <group_name>        Create a new group
  delete-group <group_name>        Delete a group
  add-member <group> <username>    Add user to group
  remove-member <group> <username> Remove user from group

Permissions:
  grant org <action> <pattern>              Grant to entire org
  grant user <username> <action> <pattern>  Grant to specific user
  grant group <group> <action> <pattern>    Grant to group
  revoke <grant_id>                         Revoke a permission
  list [target_type] [action]               List permissions
  list-permissions                          List current user's permissions

Subscriptions:
  subscribe <key_name>             Subscribe to changes on a key
  unsubscribe <key_name>           Unsubscribe from a key
  list-subscriptions               List active subscriptions

Actions: read, create, update, delete
Patterns: Namespace prefix (e.g., "christine/shared/" matches all keys under that path)

Namespace Organization:
  <username>/
  ├── private/     -> Only this user
  ├── shared/      -> Shared with others
  └── public/      -> Read-only knowledge

Examples:
  ./scripts/shared-memory.sh create-user mark
  ./scripts/shared-memory.sh create-group family
  ./scripts/shared-memory.sh add-member family mark
  ./scripts/shared-memory.sh grant group family read christine/shared/
  ./scripts/shared-memory.sh subscribe christine/shared/shopping-list
EOF
    ;;
esac
