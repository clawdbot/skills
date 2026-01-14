#!/bin/bash
# List recent emails from a mailbox
# Usage: mail-list.sh [mailbox] [account] [limit]

MAILBOX="${1:-INBOX}"
ACCOUNT="${2:-}"
LIMIT="${3:-10}"

if [ -n "$ACCOUNT" ]; then
    osascript <<EOF
tell application "Mail"
    set output to ""
    set targetMailbox to mailbox "$MAILBOX" of account "$ACCOUNT"
    set msgs to messages 1 through $LIMIT of targetMailbox
    repeat with m in msgs
        set mid to id of m
        set msubject to subject of m
        set msender to sender of m
        set mdate to date received of m
        set mread to read status of m
        set readFlag to "●"
        if mread then set readFlag to " "
        set output to output & mid & " | " & readFlag & " | " & mdate & " | " & msender & " | " & msubject & linefeed
    end repeat
    return output
end tell
EOF
else
    osascript <<EOF
tell application "Mail"
    set output to ""
    set allAccounts to every account
    set foundMsgs to {}
    repeat with acct in allAccounts
        try
            set targetMailbox to mailbox "$MAILBOX" of acct
            set msgs to messages 1 through $LIMIT of targetMailbox
            repeat with m in msgs
                set end of foundMsgs to m
            end repeat
        end try
    end repeat
    set sortedMsgs to foundMsgs
    set countLimit to $LIMIT
    if (count of sortedMsgs) < countLimit then set countLimit to (count of sortedMsgs)
    repeat with i from 1 to countLimit
        set m to item i of sortedMsgs
        set mid to id of m
        set msubject to subject of m
        set msender to sender of m
        set mdate to date received of m
        set mread to read status of m
        set readFlag to "●"
        if mread then set readFlag to " "
        set output to output & mid & " | " & readFlag & " | " & mdate & " | " & msender & " | " & msubject & linefeed
    end repeat
    return output
end tell
EOF
fi
