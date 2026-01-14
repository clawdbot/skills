#!/bin/bash
# List mailboxes for an account
# Usage: mail-mailboxes.sh [account]

ACCOUNT="${1:-}"

if [ -n "$ACCOUNT" ]; then
    osascript <<EOF
tell application "Mail"
    set output to ""
    set acct to account "$ACCOUNT"
    repeat with mbox in every mailbox of acct
        set mboxName to name of mbox
        set msgCount to count of messages of mbox
        set output to output & mboxName & " (" & msgCount & " messages)" & linefeed
    end repeat
    return output
end tell
EOF
else
    osascript <<EOF
tell application "Mail"
    set output to ""
    repeat with acct in every account
        set acctName to name of acct
        set output to output & "=== " & acctName & " ===" & linefeed
        repeat with mbox in every mailbox of acct
            set mboxName to name of mbox
            try
                set msgCount to count of messages of mbox
                set output to output & "  " & mboxName & " (" & msgCount & " messages)" & linefeed
            on error
                set output to output & "  " & mboxName & linefeed
            end try
        end repeat
        set output to output & linefeed
    end repeat
    return output
end tell
EOF
fi
