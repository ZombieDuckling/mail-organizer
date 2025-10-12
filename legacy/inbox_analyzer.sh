#!/bin/bash

echo "🔍 INBOX ANALYSIS - WHAT'S ACTUALLY IN THERE?"
echo "============================================="
echo ""

CURRENT_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
echo "📊 Total emails: $CURRENT_COUNT"
echo ""

# Get sample of subjects
echo "📧 Sample email subjects (first 20):"
osascript -e 'tell application "Mail"' -e 'set inboxMessages to messages of inbox' -e 'set count to 0' -e 'repeat with msg in inboxMessages' -e 'if count < 20 then' -e 'set count to count + 1' -e 'return subject of msg' -e 'end if' -e 'end repeat' -e 'end tell' | head -20

echo ""
echo "👤 Sample senders (first 20):"
osascript -e 'tell application "Mail"' -e 'set inboxMessages to messages of inbox' -e 'set count to 0' -e 'repeat with msg in inboxMessages' -e 'if count < 20 then' -e 'set count to count + 1' -e 'return sender of msg' -e 'end if' -e 'end repeat' -e 'end tell' | head -20

echo ""
echo "📅 Sample dates (first 20):"
osascript -e 'tell application "Mail"' -e 'set inboxMessages to messages of inbox' -e 'set count to 0' -e 'repeat with msg in inboxMessages' -e 'if count < 20 then' -e 'set count to count + 1' -e 'return date received of msg' -e 'end if' -e 'end repeat' -e 'end tell' | head -20

echo ""
echo "💡 Based on this analysis, we can create targeted cleanup scripts!"
