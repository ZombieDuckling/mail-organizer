#!/bin/bash

echo "🍎 Apple Mail Organizer"
echo "======================="
echo ""
echo "This will help you organize your Apple Mail inbox by removing promotional emails."
echo ""

# Check if Mail is running
if ! pgrep -x "Mail" > /dev/null; then
    echo "⚠️  Apple Mail is not running. Starting Mail..."
    open -a Mail
    sleep 3
fi

echo "🚀 Running email organization script..."
echo ""

# Run the AppleScript
osascript mail_organizer.scpt

echo ""
echo "✅ Email organization complete!"
echo ""
echo "💡 Tips:"
echo "   - Check your Trash folder to review deleted emails"
echo "   - You can restore any emails you want to keep"
echo "   - Run this script regularly to keep your inbox clean"
