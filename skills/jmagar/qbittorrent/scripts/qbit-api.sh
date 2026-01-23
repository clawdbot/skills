#!/bin/bash
# qBittorrent WebUI API helper script
# Usage: qbit-api.sh <command> [args...]

set -euo pipefail

CONFIG_FILE="${QBIT_CONFIG:-$HOME/.clawdbot/credentials/qbittorrent/config.json}"
COOKIE_FILE="${QBIT_COOKIE:-/tmp/qbit_cookie_$(id -u).txt}"

# Load config
if [[ -f "$CONFIG_FILE" ]]; then
    QBIT_URL=$(jq -r '.url // empty' "$CONFIG_FILE")
    QBIT_USER=$(jq -r '.username // empty' "$CONFIG_FILE")
    QBIT_PASS=$(jq -r '.password // empty' "$CONFIG_FILE")
fi

QBIT_URL="${QBIT_URL:-}"
QBIT_USER="${QBIT_USER:-}"
QBIT_PASS="${QBIT_PASS:-}"

if [[ -z "$QBIT_URL" ]]; then
    echo "Error: QBIT_URL must be set (via env or $CONFIG_FILE)" >&2
    exit 1
fi

# Remove trailing slash
QBIT_URL="${QBIT_URL%/}"

# Login and get session cookie
do_login() {
    local resp
    resp=$(curl -sS -i -X POST \
        -H "Referer: $QBIT_URL" \
        -d "username=$QBIT_USER&password=$QBIT_PASS" \
        "$QBIT_URL/api/v2/auth/login" 2>&1)
    
    if echo "$resp" | grep -iq "set-cookie: SID="; then
        local sid
        sid=$(echo "$resp" | grep -ioP 'SID=\K[^;]+')
        echo "$sid" > "$COOKIE_FILE"
        return 0
    else
        echo "Login failed" >&2
        return 1
    fi
}

# Ensure we have a valid session
ensure_session() {
    if [[ ! -f "$COOKIE_FILE" ]]; then
        do_login
        return
    fi
    
    # Test session validity
    local sid
    sid=$(cat "$COOKIE_FILE")
    local resp
    resp=$(curl -sS -o /dev/null -w "%{http_code}" \
        --cookie "SID=$sid" \
        "$QBIT_URL/api/v2/app/version")
    
    if [[ "$resp" != "200" ]]; then
        do_login
    fi
}

api_call() {
    local method="$1"
    local endpoint="$2"
    shift 2
    
    ensure_session
    local sid
    sid=$(cat "$COOKIE_FILE")
    
    curl -sS -X "$method" \
        --cookie "SID=$sid" \
        -H "Referer: $QBIT_URL" \
        "$@" \
        "${QBIT_URL}${endpoint}"
}

usage() {
    cat <<EOF
qBittorrent WebUI API CLI

Usage: $(basename "$0") <command> [options]

Commands:
  list [--filter F] [--category C] [--tag T] [--sort S] [--limit N]
  info <hash>                    Get torrent properties
  files <hash>                   Get torrent files
  trackers <hash>                Get torrent trackers
  
  add <url|magnet> [--category C] [--tags T] [--paused] [--skip-check]
  add-file <path> [--category C] [--tags T] [--paused]
  
  pause <hash|all>               Pause torrent(s)
  resume <hash|all>              Resume torrent(s)
  delete <hash> [--files]        Delete torrent (optionally with files)
  recheck <hash>                 Recheck torrent
  reannounce <hash>              Reannounce to trackers
  
  set-category <hash> <category>
  add-tags <hash> <tags>
  remove-tags <hash> <tags>
  
  categories                     List categories
  tags                           List tags
  
  transfer                       Global transfer info
  speedlimit                     Get speed limits
  set-speedlimit [--down D] [--up U]   Set limits (e.g., 5M, 1024K)
  toggle-alt-speed               Toggle alternative speed limits
  
  version                        App version
  preferences                    App preferences

Filters: all, downloading, seeding, completed, paused, active, inactive, stalled, stalled_uploading, stalled_downloading, errored

Examples:
  $(basename "$0") list --filter downloading
  $(basename "$0") add "magnet:?xt=..." --category movies
  $(basename "$0") pause all
  $(basename "$0") set-speedlimit --down 10M
EOF
}

cmd_list() {
    local filter="" category="" tag="" sort="" limit="" offset=""
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --filter|-f) filter="$2"; shift 2 ;;
            --category|-c) category="$2"; shift 2 ;;
            --tag|-t) tag="$2"; shift 2 ;;
            --sort|-s) sort="$2"; shift 2 ;;
            --limit|-l) limit="$2"; shift 2 ;;
            --offset|-o) offset="$2"; shift 2 ;;
            *) echo "Unknown option: $1" >&2; exit 1 ;;
        esac
    done
    
    local params=()
    [[ -n "$filter" ]] && params+=("filter=$filter")
    [[ -n "$category" ]] && params+=("category=$category")
    [[ -n "$tag" ]] && params+=("tag=$tag")
    [[ -n "$sort" ]] && params+=("sort=$sort")
    [[ -n "$limit" ]] && params+=("limit=$limit")
    [[ -n "$offset" ]] && params+=("offset=$offset")
    
    local query=""
    if [[ ${#params[@]} -gt 0 ]]; then
        query="?$(IFS='&'; echo "${params[*]}")"
    fi
    
    api_call GET "/api/v2/torrents/info${query}"
}

cmd_info() {
    local hash="$1"
    api_call GET "/api/v2/torrents/properties?hash=$hash"
}

cmd_files() {
    local hash="$1"
    api_call GET "/api/v2/torrents/files?hash=$hash"
}

cmd_trackers() {
    local hash="$1"
    api_call GET "/api/v2/torrents/trackers?hash=$hash"
}

cmd_add() {
    local url="$1"; shift
    local category="" tags="" paused="false" skip_check="false"
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --category|-c) category="$2"; shift 2 ;;
            --tags|-t) tags="$2"; shift 2 ;;
            --paused|-p) paused="true"; shift ;;
            --skip-check) skip_check="true"; shift ;;
            *) echo "Unknown option: $1" >&2; exit 1 ;;
        esac
    done
    
    local data="urls=$url&paused=$paused&skip_checking=$skip_check"
    [[ -n "$category" ]] && data+="&category=$category"
    [[ -n "$tags" ]] && data+="&tags=$tags"
    
    api_call POST "/api/v2/torrents/add" -d "$data"
    echo '{"status": "ok"}'
}

cmd_add_file() {
    local filepath="$1"; shift
    local category="" tags="" paused="false"
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --category|-c) category="$2"; shift 2 ;;
            --tags|-t) tags="$2"; shift 2 ;;
            --paused|-p) paused="true"; shift ;;
            *) echo "Unknown option: $1" >&2; exit 1 ;;
        esac
    done
    
    ensure_session
    local sid
    sid=$(cat "$COOKIE_FILE")
    
    local args=(-F "torrents=@$filepath" -F "paused=$paused")
    [[ -n "$category" ]] && args+=(-F "category=$category")
    [[ -n "$tags" ]] && args+=(-F "tags=$tags")
    
    curl -sS --cookie "SID=$sid" -H "Referer: $QBIT_URL" "${args[@]}" "$QBIT_URL/api/v2/torrents/add"
    echo '{"status": "ok"}'
}

cmd_pause() {
    local hashes="$1"
    api_call POST "/api/v2/torrents/pause" -d "hashes=$hashes"
    echo '{"status": "ok"}'
}

cmd_resume() {
    local hashes="$1"
    api_call POST "/api/v2/torrents/resume" -d "hashes=$hashes"
    echo '{"status": "ok"}'
}

cmd_delete() {
    local hash="$1"; shift
    local delete_files="false"
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --files|-f) delete_files="true"; shift ;;
            *) echo "Unknown option: $1" >&2; exit 1 ;;
        esac
    done
    
    api_call POST "/api/v2/torrents/delete" -d "hashes=$hash&deleteFiles=$delete_files"
    echo '{"status": "ok"}'
}

cmd_recheck() {
    local hash="$1"
    api_call POST "/api/v2/torrents/recheck" -d "hashes=$hash"
    echo '{"status": "ok"}'
}

cmd_reannounce() {
    local hash="$1"
    api_call POST "/api/v2/torrents/reannounce" -d "hashes=$hash"
    echo '{"status": "ok"}'
}

cmd_set_category() {
    local hash="$1"
    local category="$2"
    api_call POST "/api/v2/torrents/setCategory" -d "hashes=$hash&category=$category"
    echo '{"status": "ok"}'
}

cmd_add_tags() {
    local hash="$1"
    local tags="$2"
    api_call POST "/api/v2/torrents/addTags" -d "hashes=$hash&tags=$tags"
    echo '{"status": "ok"}'
}

cmd_remove_tags() {
    local hash="$1"
    local tags="$2"
    api_call POST "/api/v2/torrents/removeTags" -d "hashes=$hash&tags=$tags"
    echo '{"status": "ok"}'
}

cmd_categories() {
    api_call GET "/api/v2/torrents/categories"
}

cmd_tags() {
    api_call GET "/api/v2/torrents/tags"
}

cmd_transfer() {
    api_call GET "/api/v2/transfer/info"
}

cmd_speedlimit() {
    echo "{"
    echo "  \"download\": $(api_call GET '/api/v2/transfer/downloadLimit'),"
    echo "  \"upload\": $(api_call GET '/api/v2/transfer/uploadLimit')"
    echo "}"
}

parse_speed() {
    local val="$1"
    local num="${val%[KMG]}"
    local suffix="${val: -1}"
    
    case "$suffix" in
        K|k) echo $((num * 1024)) ;;
        M|m) echo $((num * 1024 * 1024)) ;;
        G|g) echo $((num * 1024 * 1024 * 1024)) ;;
        *) echo "$val" ;;
    esac
}

cmd_set_speedlimit() {
    local down="" up=""
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --down|-d) down=$(parse_speed "$2"); shift 2 ;;
            --up|-u) up=$(parse_speed "$2"); shift 2 ;;
            *) echo "Unknown option: $1" >&2; exit 1 ;;
        esac
    done
    
    [[ -n "$down" ]] && api_call POST "/api/v2/transfer/setDownloadLimit" -d "limit=$down"
    [[ -n "$up" ]] && api_call POST "/api/v2/transfer/setUploadLimit" -d "limit=$up"
    echo '{"status": "ok"}'
}

cmd_toggle_alt_speed() {
    api_call POST "/api/v2/transfer/toggleSpeedLimitsMode"
    echo '{"status": "ok"}'
}

cmd_version() {
    api_call GET "/api/v2/app/version"
}

cmd_preferences() {
    api_call GET "/api/v2/app/preferences"
}

# Main dispatch
case "${1:-}" in
    list) shift; cmd_list "$@" ;;
    info) shift; cmd_info "$@" ;;
    files) shift; cmd_files "$@" ;;
    trackers) shift; cmd_trackers "$@" ;;
    add) shift; cmd_add "$@" ;;
    add-file) shift; cmd_add_file "$@" ;;
    pause) shift; cmd_pause "$@" ;;
    resume) shift; cmd_resume "$@" ;;
    delete) shift; cmd_delete "$@" ;;
    recheck) shift; cmd_recheck "$@" ;;
    reannounce) shift; cmd_reannounce "$@" ;;
    set-category) shift; cmd_set_category "$@" ;;
    add-tags) shift; cmd_add_tags "$@" ;;
    remove-tags) shift; cmd_remove_tags "$@" ;;
    categories) shift; cmd_categories "$@" ;;
    tags) shift; cmd_tags "$@" ;;
    transfer) shift; cmd_transfer "$@" ;;
    speedlimit) shift; cmd_speedlimit "$@" ;;
    set-speedlimit) shift; cmd_set_speedlimit "$@" ;;
    toggle-alt-speed) shift; cmd_toggle_alt_speed "$@" ;;
    version) shift; cmd_version "$@" ;;
    preferences) shift; cmd_preferences "$@" ;;
    -h|--help|help|"") usage ;;
    *) echo "Unknown command: $1" >&2; usage; exit 1 ;;
esac
