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

echo "🚀 Running mark all as read script..."
echo ""

# Run the AppleScript
osascript mark_all_read.scpt

echo ""
echo "✅ Mark as read operation complete!"
echo ""
echo "💡 All emails in your inbox are now marked as read!"
