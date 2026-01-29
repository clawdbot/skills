#!/bin/bash
#
# vault.sh - Moltbot skill wrapper for vaultctl
#
# This script is called by Moltbot to execute vault operations
# on the remote Mac via SSH tunnel.
#
# Usage:
#   ./vault.sh <command> [args...]
#
# Environment:
#   VAULT_SSH_USER  - Mac username (required)
#   VAULT_SSH_PORT  - SSH port for tunnel (default: 2222)
#   VAULT_SSH_HOST  - SSH host (default: localhost)
#

set -euo pipefail

# Auto-detect Mac username from config file if not set via env
VAULT_SSH_USER="${VAULT_SSH_USER:-}"
if [[ -z "$VAULT_SSH_USER" && -f "$HOME/.config/headless-vault-cli/mac-user" ]]; then
    VAULT_SSH_USER="$(cat "$HOME/.config/headless-vault-cli/mac-user")"
fi

VAULT_SSH_PORT="${VAULT_SSH_PORT:-2222}"
VAULT_SSH_HOST="${VAULT_SSH_HOST:-localhost}"
SSH_OPTS="-o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=accept-new"

if [[ -z "$VAULT_SSH_USER" ]]; then
    echo '{"error": "config_missing", "message": "Mac username not configured. Run tunnel-setup.sh or set VAULT_SSH_USER"}' >&2
    exit 1
fi

# Run vaultctl command on remote Mac
run_vaultctl() {
    ssh $SSH_OPTS -p "$VAULT_SSH_PORT" "${VAULT_SSH_USER}@${VAULT_SSH_HOST}" vaultctl "$@"
}

# Check if tunnel is up
check_tunnel() {
    if ! ssh $SSH_OPTS -p "$VAULT_SSH_PORT" "${VAULT_SSH_USER}@${VAULT_SSH_HOST}" vaultctl tree --depth 0 >/dev/null 2>&1; then
        echo '{"error": "tunnel_down", "message": "Cannot reach Mac. Is the tunnel running?"}' >&2
        exit 1
    fi
}

cmd="${1:-}"
shift || true

case "$cmd" in
    tree)
        args=()
        while [[ $# -gt 0 ]]; do
            case "$1" in
                depth=*) args+=(--depth "${1#depth=}") ;;
                all=true) args+=(--all) ;;
            esac
            shift
        done
        run_vaultctl tree "${args[@]}"
        ;;

    resolve)
        while [[ $# -gt 0 ]]; do
            case "$1" in
                path=*)
                    val="${1#path=}"
                    encoded=$(printf '%s' "$val" | base64)
                    run_vaultctl resolve --path "$encoded" --base64
                    exit
                    ;;
                title=*)
                    val="${1#title=}"
                    encoded=$(printf '%s' "$val" | base64)
                    run_vaultctl resolve --title "$encoded" --base64
                    exit
                    ;;
            esac
            shift
        done
        echo '{"error": "missing_param", "message": "Specify path= or title="}' >&2
        exit 1
        ;;

    info)
        path=""
        while [[ $# -gt 0 ]]; do
            case "$1" in
                path=*) path="${1#path=}" ;;
            esac
            shift
        done
        if [[ -z "$path" ]]; then
            echo '{"error": "missing_param", "message": "path= is required"}' >&2
            exit 1
        fi
        # Base64 encode path to handle spaces
        encoded_path=$(printf '%s' "$path" | base64)
        run_vaultctl info "$encoded_path" --base64
        ;;

    read)
        path=""
        while [[ $# -gt 0 ]]; do
            case "$1" in
                path=*) path="${1#path=}" ;;
            esac
            shift
        done
        if [[ -z "$path" ]]; then
            echo '{"error": "missing_param", "message": "path= is required"}' >&2
            exit 1
        fi
        # Base64 encode path to handle spaces
        encoded_path=$(printf '%s' "$path" | base64)
        run_vaultctl read "$encoded_path" --base64
        ;;

    create)
        path=""
        content=""
        while [[ $# -gt 0 ]]; do
            case "$1" in
                path=*) path="${1#path=}" ;;
                content=*) content="${1#content=}" ;;
            esac
            shift
        done
        if [[ -z "$path" || -z "$content" ]]; then
            echo '{"error": "missing_param", "message": "path= and content= are required"}' >&2
            exit 1
        fi
        # Pipe content via stdin to avoid shell quoting issues over SSH
        printf '%s' "$content" | ssh $SSH_OPTS -p "$VAULT_SSH_PORT" "${VAULT_SSH_USER}@${VAULT_SSH_HOST}" vaultctl create "$path" -
        ;;

    append)
        path=""
        content=""
        while [[ $# -gt 0 ]]; do
            case "$1" in
                path=*) path="${1#path=}" ;;
                content=*) content="${1#content=}" ;;
            esac
            shift
        done
        if [[ -z "$path" || -z "$content" ]]; then
            echo '{"error": "missing_param", "message": "path= and content= are required"}' >&2
            exit 1
        fi
        # Pipe content via stdin to avoid shell quoting issues over SSH
        printf '%s' "$content" | ssh $SSH_OPTS -p "$VAULT_SSH_PORT" "${VAULT_SSH_USER}@${VAULT_SSH_HOST}" vaultctl append "$path" -
        ;;

    check)
        check_tunnel
        echo '{"status": "ok", "message": "Tunnel is up"}'
        ;;

    *)
        echo '{"error": "unknown_command", "message": "Unknown command: '"$cmd"'", "available": ["tree", "resolve", "info", "read", "create", "append", "check"]}' >&2
        exit 1
        ;;
esac
