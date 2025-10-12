#!/bin/bash

echo "📧 Mark All Emails as Read"
echo "=========================="
echo ""

# Check if Mail is running
if ! pgrep -x "Mail" > /dev/null; then
    echo "⚠️  Apple Mail is not running. Starting Mail..."
    open -a Mail
    sleep 3
fi

echo "🚀 Marking all inbox emails as read..."

# Simple working AppleScript
osascript -e 'tell application "Mail"' -e 'set inboxMessages to messages of inbox' -e 'repeat with msg in inboxMessages' -e 'try' -e 'set read status of msg to true' -e 'on error' -e 'continue' -e 'end try' -e 'end repeat' -e 'end tell'

echo "✅ All inbox emails marked as read!"
echo ""
echo "💡 Your inbox is now clean of unread emails!"
