#!/bin/bash

echo "📧 Advanced Mark All Emails as Read"
echo "==================================="
echo ""

# Check if Mail is running
if ! pgrep -x "Mail" > /dev/null; then
    echo "⚠️  Apple Mail is not running. Starting Mail..."
    open -a Mail
    sleep 3
fi

echo "🚀 Running advanced mark all as read script..."
echo ""

# Run the AppleScript
osascript mark_all_read_advanced.scpt

echo ""
echo "✅ Advanced mark as read operation complete!"
echo ""
echo "💡 All selected emails are now marked as read!"
