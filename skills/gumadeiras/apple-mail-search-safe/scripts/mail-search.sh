#!/usr/bin/env bash
# mail-search - Fast Apple Mail search via SQLite
# Usage: mail-search <command> [args] [options]

set -e

# Find the Mail database
find_db() {
    local db
    for v in 11 10 9; do
        db="$HOME/Library/Mail/V$v/MailData/Envelope Index"
        if [[ -f "$db" ]]; then
            echo "$db"
            return 0
        fi
    done
    echo "Error: Could not find Mail database" >&2
    return 1
}

SOURCE_DB="${MAIL_DB:-$(find_db)}"

# Copy to temp file to avoid corrupting the live DB while Mail.app is running
TEMP_DB=$(mktemp -t mail-search.XXXXXX)
cleanup() {
    rm -f "$TEMP_DB" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

cp "$SOURCE_DB" "$TEMP_DB"
DB="$TEMP_DB"
LIMIT=20
FORMAT="table"

# Parse global options
while [[ $# -gt 0 ]]; do
    case "$1" in
        -n|--limit) LIMIT="$2"; shift 2 ;;
        -j|--json) FORMAT="json"; shift ;;
        -c|--csv) FORMAT="csv"; shift ;;
        -q|--quiet) QUIET=1; shift ;;
        --db) DB="$2"; shift 2 ;;
        -*) echo "Unknown option: $1" >&2; exit 1 ;;
        *) break ;;
    esac
done

CMD="${1:-help}"
shift || true

# Output formatting
output_query() {
    local query="$1"
    case "$FORMAT" in
        json)
            sqlite3 -json "$DB" "$query" 2>/dev/null || sqlite3 "$DB" "$query"
            ;;
        csv)
            sqlite3 -csv -header "$DB" "$query"
            ;;
        table)
            sqlite3 -header -column "$DB" "$query"
            ;;
    esac
}

case "$CMD" in
    subject)
        PATTERN="${1:-%}"
        output_query "
            SELECT m.ROWID as id, 
                   datetime(m.date_sent, 'unixepoch', 'localtime') as date,
                   a.address as sender,
                   s.subject
            FROM messages m
            JOIN subjects s ON m.subject = s.ROWID
            LEFT JOIN addresses a ON m.sender = a.ROWID
            WHERE s.subject LIKE '%${PATTERN}%'
            ORDER BY m.date_sent DESC
            LIMIT $LIMIT;
        "
        ;;
    
    sender|from)
        PATTERN="${1:-%}"
        output_query "
            SELECT m.ROWID as id,
                   datetime(m.date_sent, 'unixepoch', 'localtime') as date,
                   a.address as sender,
                   s.subject
            FROM messages m
            JOIN subjects s ON m.subject = s.ROWID
            LEFT JOIN addresses a ON m.sender = a.ROWID
            WHERE a.address LIKE '%${PATTERN}%'
            ORDER BY m.date_sent DESC
            LIMIT $LIMIT;
        "
        ;;
    
    from-name)
        PATTERN="${1:-%}"
        output_query "
            SELECT m.ROWID as id,
                   datetime(m.date_sent, 'unixepoch', 'localtime') as date,
                   a.comment as name,
                   a.address as sender,
                   s.subject
            FROM messages m
            JOIN subjects s ON m.subject = s.ROWID
            LEFT JOIN addresses a ON m.sender = a.ROWID
            WHERE a.comment LIKE '%${PATTERN}%'
            ORDER BY m.date_sent DESC
            LIMIT $LIMIT;
        "
        ;;
    
    to)
        PATTERN="${1:-%}"
        output_query "
            SELECT m.ROWID as id,
                   datetime(m.date_sent, 'unixepoch', 'localtime') as date,
                   a.address as sender,
                   s.subject
            FROM messages m
            JOIN subjects s ON m.subject = s.ROWID
            LEFT JOIN addresses a ON m.sender = a.ROWID
            JOIN recipients r ON m.ROWID = r.message
            JOIN addresses ra ON r.address = ra.ROWID
            WHERE ra.address LIKE '%${PATTERN}%'
            ORDER BY m.date_sent DESC
            LIMIT $LIMIT;
        "
        ;;
    
    unread)
        output_query "
            SELECT m.ROWID as id,
                   datetime(m.date_sent, 'unixepoch', 'localtime') as date,
                   a.address as sender,
                   s.subject
            FROM messages m
            JOIN subjects s ON m.subject = s.ROWID
            LEFT JOIN addresses a ON m.sender = a.ROWID
            WHERE m.read = 0 AND m.deleted = 0
            ORDER BY m.date_sent DESC
            LIMIT $LIMIT;
        "
        ;;
    
    attachments)
        output_query "
            SELECT DISTINCT m.ROWID as id,
                   datetime(m.date_sent, 'unixepoch', 'localtime') as date,
                   a.address as sender,
                   s.subject,
                   att.name as attachment
            FROM messages m
            JOIN subjects s ON m.subject = s.ROWID
            LEFT JOIN addresses a ON m.sender = a.ROWID
            JOIN attachments att ON m.ROWID = att.message
            ORDER BY m.date_sent DESC
            LIMIT $LIMIT;
        "
        ;;
    
    attachment-type)
        EXT="${1:-pdf}"
        output_query "
            SELECT DISTINCT m.ROWID as id,
                   datetime(m.date_sent, 'unixepoch', 'localtime') as date,
                   a.address as sender,
                   s.subject,
                   att.name as attachment
            FROM messages m
            JOIN subjects s ON m.subject = s.ROWID
            LEFT JOIN addresses a ON m.sender = a.ROWID
            JOIN attachments att ON m.ROWID = att.message
            WHERE att.name LIKE '%.${EXT}'
            ORDER BY m.date_sent DESC
            LIMIT $LIMIT;
        "
        ;;
    
    recent)
        DAYS="${1:-7}"
        SINCE=$(($(date +%s) - DAYS * 86400))
        output_query "
            SELECT m.ROWID as id,
                   datetime(m.date_sent, 'unixepoch', 'localtime') as date,
                   a.address as sender,
                   s.subject
            FROM messages m
            JOIN subjects s ON m.subject = s.ROWID
            LEFT JOIN addresses a ON m.sender = a.ROWID
            WHERE m.date_sent >= $SINCE AND m.deleted = 0
            ORDER BY m.date_sent DESC
            LIMIT $LIMIT;
        "
        ;;
    
    date-range)
        START_DATE="${1:-1970-01-01}"
        END_DATE="${2:-2099-12-31}"
        START_TS=$(date -j -f "%Y-%m-%d" "$START_DATE" "+%s" 2>/dev/null || date -d "$START_DATE" "+%s")
        END_TS=$(date -j -f "%Y-%m-%d" "$END_DATE" "+%s" 2>/dev/null || date -d "$END_DATE" "+%s")
        END_TS=$((END_TS + 86400))  # Include the end date
        output_query "
            SELECT m.ROWID as id,
                   datetime(m.date_sent, 'unixepoch', 'localtime') as date,
                   a.address as sender,
                   s.subject
            FROM messages m
            JOIN subjects s ON m.subject = s.ROWID
            LEFT JOIN addresses a ON m.sender = a.ROWID
            WHERE m.date_sent >= $START_TS AND m.date_sent < $END_TS AND m.deleted = 0
            ORDER BY m.date_sent DESC
            LIMIT $LIMIT;
        "
        ;;
    
    open)
        MSG_ID="$1"
        if [[ -z "$MSG_ID" ]]; then
            echo "Usage: mail-search open <message_id>" >&2
            exit 1
        fi
        # Get the message-id header for the message
        MSG_URI=$(sqlite3 "$DB" "SELECT document_id FROM messages WHERE ROWID = $MSG_ID;")
        if [[ -n "$MSG_URI" ]]; then
            open "message://%3c${MSG_URI}%3e"
        else
            echo "Message not found" >&2
            exit 1
        fi
        ;;

    body)
        MSG_ID="$1"
        if [[ -z "$MSG_ID" ]]; then
            echo "Usage: mail-search body <message_id>" >&2
            exit 1
        fi
        osascript << EOF
tell application "Mail"
    set msg to first message of inbox whose id is $MSG_ID
    set output to "From: " & sender of msg & linefeed
    set output to output & "Subject: " & subject of msg & linefeed
    set output to output & "Date: " & date sent of msg & linefeed & linefeed
    set output to output & "Content:" & linefeed & content of msg
    return output
end tell
EOF
        ;;

    stats)
        echo "=== Mail Database Statistics ==="
        echo ""
        echo "Total messages: $(sqlite3 "$DB" "SELECT COUNT(*) FROM messages;")"
        echo "Unread: $(sqlite3 "$DB" "SELECT COUNT(*) FROM messages WHERE read = 0 AND deleted = 0;")"
        echo "Deleted: $(sqlite3 "$DB" "SELECT COUNT(*) FROM messages WHERE deleted = 1;")"
        echo "With attachments: $(sqlite3 "$DB" "SELECT COUNT(DISTINCT message) FROM attachments;")"
        echo ""
        echo "Database: $SOURCE_DB"
        echo "Size: $(du -h "$SOURCE_DB" | cut -f1)"
        ;;
    
    query)
        # Raw SQL query
        output_query "$1"
        ;;
    
    help|--help|-h)
        cat << 'EOF'
mail-search - Fast Apple Mail search via SQLite

Usage: mail-search [options] <command> [args]

Commands:
  subject <pattern>           Search by subject
  sender <pattern>            Search by sender email
  from-name <pattern>         Search by sender display name
  to <pattern>                Search by recipient
  unread                      List unread emails
  attachments                 List emails with attachments
  attachment-type <ext>       Find by attachment type (pdf, docx, etc)
  recent <days>               Emails from last N days (default: 7)
  date-range <start> <end>    Emails between dates (YYYY-MM-DD)
  open <id>                   Open email in Mail.app
  body <id>                   Read full email body (AppleScript)
  stats                       Database statistics
  query "<sql>"               Run raw SQL query

Options:
  -n, --limit N     Max results (default: 20)
  -j, --json        Output as JSON
  -c, --csv         Output as CSV
  -q, --quiet       Minimal output
  --db PATH         Override database path

Examples:
  mail-search subject "invoice" -n 50
  mail-search sender "@amazon.com" --json
  mail-search recent 30 --csv > emails.csv
  mail-search unread
EOF
        ;;
    
    *)
        echo "Unknown command: $CMD" >&2
        echo "Run 'mail-search help' for usage" >&2
        exit 1
        ;;
esac
