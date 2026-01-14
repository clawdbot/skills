#!/bin/bash
# Reply to an email by message ID
# Usage: mail-reply.sh <message-id> "Reply body" [reply-all]

MSG_ID="${1:-}"
REPLY_BODY="${2:-}"
REPLY_ALL="${3:-false}"

if [ -z "$MSG_ID" ] || [ -z "$REPLY_BODY" ]; then
    echo "Usage: mail-reply.sh <message-id> \"Reply body\" [reply-all]"
    exit 1
fi

REPLY_BODY_ESCAPED=$(echo "$REPLY_BODY" | sed 's/"/\\"/g')

osascript <<EOF
tell application "Mail"
    set foundMsg to missing value
    
    -- Search all accounts for the message
    repeat with acct in every account
        repeat with mbox in every mailbox of acct
            try
                set msgs to (messages of mbox whose id is $MSG_ID)
                if (count of msgs) > 0 then
                    set foundMsg to item 1 of msgs
                    exit repeat
                end if
            end try
        end repeat
        if foundMsg is not missing value then exit repeat
    end repeat
    
    if foundMsg is missing value then
        return "Message not found with ID: $MSG_ID"
    end if
    
    if "$REPLY_ALL" is "true" then
        set replyMsg to reply foundMsg with opening window and reply to all
    else
        set replyMsg to reply foundMsg with opening window
    end if
    
    set oldContent to content of replyMsg
    set content of replyMsg to "$REPLY_BODY_ESCAPED" & return & return & oldContent
    send replyMsg
    
    return "Reply sent"
end tell
EOF
