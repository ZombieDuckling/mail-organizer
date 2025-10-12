#!/bin/bash

echo "🍎 Smart Mail Organizer with Unsubscribe Detection"
echo "=================================================="
echo ""

# Check if Mail is running
if ! pgrep -x "Mail" > /dev/null; then
    echo "⚠️  Apple Mail is not running. Starting Mail..."
    open -a Mail
    sleep 3
fi

echo "📊 Current inbox status:"
INBOX_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
echo "   Messages in inbox: $INBOX_COUNT"
echo ""

echo "🤔 What would you like to do?"
echo "1. Quick cleanup (delete promotional emails)"
echo "2. Smart cleanup (preserve emails with unsubscribe links)"
echo "3. Analyze unsubscribe links only"
echo "4. Advanced unsubscribe processor (Python)"
echo "5. Create automatic mail rules"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🚀 Running quick cleanup..."
        osascript -e 'tell application "Mail"' -e 'set inboxMessages to messages of inbox' -e 'set deletedCount to 0' -e 'repeat with msg in inboxMessages' -e 'set msgSubject to subject of msg' -e 'set msgSender to sender of msg' -e 'set isPromo to false' -e 'if msgSubject contains "promotional" or msgSubject contains "marketing" or msgSubject contains "newsletter" or msgSubject contains "offers" or msgSubject contains "sale" or msgSubject contains "discount" or msgSubject contains "deal" or msgSubject contains "unsubscribe" then' -e 'set isPromo to true' -e 'else if msgSender contains "noreply" or msgSender contains "no-reply" or msgSender contains "marketing" or msgSender contains "promo" or msgSender contains "offers" or msgSender contains "deals" or msgSender contains "newsletter" or msgSender contains "notifications" then' -e 'set isPromo to true' -e 'end if' -e 'if isPromo then' -e 'delete msg' -e 'set deletedCount to deletedCount + 1' -e 'end if' -e 'end repeat' -e 'display dialog "Deleted " & deletedCount & " promotional emails!" buttons {"OK"}' -e 'end tell'
        ;;
    2)
        echo "🧠 Running smart cleanup (preserving unsubscribe emails)..."
        osascript enhanced_organizer.scpt
        ;;
    3)
        echo "🔍 Analyzing unsubscribe links..."
        osascript unsubscribe_extractor.scpt
        ;;
    4)
        echo "🐍 Running advanced unsubscribe processor..."
        python3 unsubscribe_processor.py
        ;;
    5)
        echo "⚙️  Creating automatic mail rules..."
        osascript create_mail_rules.scpt
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "✅ Operation complete!"
echo ""
echo "💡 Tips:"
echo "   - Check your Trash folder to review deleted emails"
echo "   - You can restore any emails you want to keep"
echo "   - Run this script regularly to keep your inbox clean"
echo "   - Use option 3 or 4 to handle unsubscribe links properly"
