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

# Create a simple AppleScript file
cat > /tmp/mark_read.scpt << 'SCRIPT_EOF'
tell application "Mail"
    set inboxMessages to messages of inbox
    repeat with msg in inboxMessages
        try
            set read status of msg to true
        on error
            continue
        end try
    end repeat
end tell
SCRIPT_EOF

# Run the script
osascript /tmp/mark_read.scpt

echo "✅ All inbox emails marked as read!"
echo ""
echo "💡 Your inbox is now clean of unread emails!"
