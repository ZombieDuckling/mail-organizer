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

# Simple one-liner that should work
osascript -e 'tell application "Mail" to set read status of every message of inbox to true'

echo "✅ All inbox emails marked as read!"
echo ""
echo "💡 Your inbox is now clean of unread emails!"
