#!/bin/bash
# Search emails by subject/sender/content
# Usage: mail-search.sh "query" [mailbox] [limit]

QUERY="${1:-}"
MAILBOX="${2:-}"
LIMIT="${3:-20}"

if [ -z "$QUERY" ]; then
    echo "Usage: mail-search.sh \"query\" [mailbox] [limit]"
    exit 1
fi

osascript <<EOF
tell application "Mail"
    set output to ""
    set foundMsgs to {}
    set searchQuery to "$QUERY"
    set limitCount to $LIMIT
    
    if "$MAILBOX" is not "" then
        -- Search specific mailbox across accounts
        repeat with acct in every account
            try
                set targetMailbox to mailbox "$MAILBOX" of acct
                set msgs to (messages of targetMailbox whose subject contains searchQuery or sender contains searchQuery)
                repeat with m in msgs
                    set end of foundMsgs to m
                end repeat
            end try
        end repeat
    else
        -- Search all mailboxes
        repeat with acct in every account
            repeat with mbox in every mailbox of acct
                try
                    set msgs to (messages of mbox whose subject contains searchQuery or sender contains searchQuery)
                    repeat with m in msgs
                        set end of foundMsgs to m
                    end repeat
                end try
            end repeat
        end repeat
    end if
    
    if (count of foundMsgs) < limitCount then set limitCount to (count of foundMsgs)
    
    repeat with i from 1 to limitCount
        set m to item i of foundMsgs
        set mid to id of m
        set msubject to subject of m
        set msender to sender of m
        set mdate to date received of m
        set mread to read status of m
        set readFlag to "●"
        if mread then set readFlag to " "
        set output to output & mid & " | " & readFlag & " | " & mdate & " | " & msender & " | " & msubject & linefeed
    end repeat
    
    if output is "" then
        return "No emails found matching: " & searchQuery
    end if
    return output
end tell
EOF
