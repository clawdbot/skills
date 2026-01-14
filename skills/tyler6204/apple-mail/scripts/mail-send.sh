#!/bin/bash
# Send an email via Mail.app
# Usage: mail-send.sh "to@email.com" "Subject" "Body" [from-account] [attachment]

TO="${1:-}"
SUBJECT="${2:-}"
BODY="${3:-}"
FROM_ACCOUNT="${4:-}"
ATTACHMENT="${5:-}"

if [ -z "$TO" ] || [ -z "$SUBJECT" ] || [ -z "$BODY" ]; then
    echo "Usage: mail-send.sh \"to@email.com\" \"Subject\" \"Body\" [from-account] [attachment]"
    echo "  All three arguments (to, subject, body) are required."
    exit 1
fi

# Escape quotes in body
BODY_ESCAPED=$(echo "$BODY" | sed 's/"/\\"/g')
SUBJECT_ESCAPED=$(echo "$SUBJECT" | sed 's/"/\\"/g')

if [ -n "$FROM_ACCOUNT" ] && [ -n "$ATTACHMENT" ]; then
    osascript <<EOF
tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:"$SUBJECT_ESCAPED", content:"$BODY_ESCAPED", visible:false}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"$TO"}
        set sender to "$FROM_ACCOUNT"
        tell content
            make new attachment with properties {file name:POSIX file "$ATTACHMENT"} at after last paragraph
        end tell
    end tell
    send newMessage
    return "Email sent to $TO"
end tell
EOF
elif [ -n "$FROM_ACCOUNT" ]; then
    osascript <<EOF
tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:"$SUBJECT_ESCAPED", content:"$BODY_ESCAPED", visible:false}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"$TO"}
        set sender to "$FROM_ACCOUNT"
    end tell
    send newMessage
    return "Email sent to $TO"
end tell
EOF
elif [ -n "$ATTACHMENT" ]; then
    osascript <<EOF
tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:"$SUBJECT_ESCAPED", content:"$BODY_ESCAPED", visible:false}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"$TO"}
        tell content
            make new attachment with properties {file name:POSIX file "$ATTACHMENT"} at after last paragraph
        end tell
    end tell
    send newMessage
    return "Email sent to $TO"
end tell
EOF
else
    osascript <<EOF
tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:"$SUBJECT_ESCAPED", content:"$BODY_ESCAPED", visible:false}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"$TO"}
    end tell
    send newMessage
    return "Email sent to $TO"
end tell
EOF
fi
