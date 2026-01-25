#!/bin/bash

# IMAP Email Skill Setup Helper

echo "🦞 IMAP Email Skill Setup"
echo ""
echo "Setting up ProtonMail Bridge configuration..."
echo ""

# Check if Bridge is running
if ! ps aux | grep -i "proton.*bridge" | grep -v grep > /dev/null; then
    echo "❌ ProtonMail Bridge doesn't appear to be running"
    echo "   Please start ProtonMail Bridge first"
    exit 1
fi

echo "✅ ProtonMail Bridge is running"
echo ""

# Prompt for credentials
echo "Please enter your ProtonMail IMAP settings from Bridge:"
echo ""
read -p "IMAP Email address: " EMAIL
read -p "IMAP Port (default 1143): " PORT
PORT=${PORT:-1143}
read -s -p "IMAP Password (from Bridge): " PASSWORD
echo ""

# Create .env file
cat > .env << EOF
# IMAP Email Configuration
# Generated: $(date)

IMAP_HOST=127.0.0.1
IMAP_PORT=$PORT
IMAP_USER=$EMAIL
IMAP_PASS=$PASSWORD
IMAP_TLS=false
IMAP_MAILBOX=INBOX
EOF

echo ""
echo "✅ Created .env file"
echo ""
echo "Testing connection..."
echo ""

# Test the connection
if node scripts/imap.js list-mailboxes 2>&1 | grep -q "name"; then
    echo "✅ IMAP connection successful!"
    echo ""
    echo "Try checking for emails:"
    echo "  node scripts/imap.js check"
    echo ""
else
    echo "❌ Connection test failed"
    echo ""
    echo "Troubleshooting:"
    echo "1. Verify Bridge is running and logged in"
    echo "2. Check the IMAP settings in Bridge app (Settings → IMAP/SMTP)"
    echo "3. Make sure you're using the Bridge-generated password, not your ProtonMail password"
    echo "4. Verify port $PORT is correct (check Bridge settings)"
fi
