#!/bin/bash
# Read full email content by message ID
# Usage: mail-read.sh <message-id>

MSG_ID="${1:-}"

if [ -z "$MSG_ID" ]; then
    echo "Usage: mail-read.sh <message-id>"
    exit 1
fi

osascript <<EOF
tell application "Mail"
    set output to ""
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
    
    set m to foundMsg
    set msubject to subject of m
    set msender to sender of m
    set mto to ""
    try
        set recipList to to recipients of m
        repeat with r in recipList
            set mto to mto & address of r & ", "
        end repeat
        if mto ends with ", " then set mto to text 1 thru -3 of mto
    end try
    set mdate to date received of m
    set mcontent to content of m
    
    set output to "From: " & msender & linefeed
    set output to output & "To: " & mto & linefeed
    set output to output & "Date: " & mdate & linefeed
    set output to output & "Subject: " & msubject & linefeed
    set output to output & linefeed & "---" & linefeed & linefeed
    set output to output & mcontent
    
    return output
end tell
EOF
