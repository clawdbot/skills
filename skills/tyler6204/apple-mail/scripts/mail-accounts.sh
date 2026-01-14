#!/bin/bash
# List configured email accounts
# Usage: mail-accounts.sh

osascript <<EOF
tell application "Mail"
    set output to ""
    repeat with acct in every account
        set acctName to name of acct
        set acctType to account type of acct as string
        set acctEmail to ""
        try
            set acctEmail to email addresses of acct
            if class of acctEmail is list then
                set acctEmail to item 1 of acctEmail
            end if
        end try
        set output to output & acctName & " (" & acctType & ") - " & acctEmail & linefeed
    end repeat
    return output
end tell
EOF
