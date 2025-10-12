#!/bin/bash

echo "📧 Quick Mark All as Read"
echo "========================="
echo ""

# Quick one-liner to mark all inbox emails as read
echo "🚀 Marking all inbox emails as read..."
osascript -e 'tell application "Mail"' -e 'set inboxMessages to messages of inbox' -e 'repeat with msg in inboxMessages' -e 'try' -e 'set read status of msg to true' -e 'on error' -e 'continue' -e 'end try' -e 'end repeat' -e 'end tell'

echo "✅ All inbox emails marked as read!"
echo ""
echo "💡 To mark all emails in all mailboxes as read, run:"
echo "   ./mark_all_read_advanced.sh"
