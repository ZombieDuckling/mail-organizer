#!/bin/bash

echo "🚀 MEGA EMAIL CLEANUP - 100% CLEAN INBOX"
echo "========================================"
echo ""

# Check current count
CURRENT_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
echo "📊 Starting with: $CURRENT_COUNT emails"
echo ""

# Function to run cleanup and show results
cleanup_and_show() {
    local keyword="$1"
    local description="$2"
    
    echo "🧹 Cleaning $description..."
    
    # Run cleanup
    osascript -e "tell application \"Mail\"" -e "set inboxMessages to messages of inbox" -e "set deletedCount to 0" -e "repeat with msg in inboxMessages" -e "try" -e "if subject of msg contains \"$keyword\" then" -e "delete msg" -e "set deletedCount to deletedCount + 1" -e "end if" -e "on error" -e "continue" -e "end try" -e "end repeat" -e "return deletedCount" -e "end tell" > /tmp/deleted_count.txt 2>/dev/null
    
    DELETED=$(cat /tmp/deleted_count.txt 2>/dev/null || echo "0")
    echo "   ✅ Deleted $DELETED $description"
    
    # Get new count
    NEW_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    echo "   📊 Remaining: $NEW_COUNT emails"
    echo ""
}

# Run multiple cleanups
cleanup_and_show "newsletter" "newsletter emails"
cleanup_and_show "promotional" "promotional emails"
cleanup_and_show "marketing" "marketing emails"
cleanup_and_show "offers" "offer emails"
cleanup_and_show "sale" "sale emails"
cleanup_and_show "discount" "discount emails"
cleanup_and_show "deal" "deal emails"
cleanup_and_show "unsubscribe" "unsubscribe emails"
cleanup_and_show "limited time" "limited time emails"
cleanup_and_show "exclusive" "exclusive emails"
cleanup_and_show "special offer" "special offer emails"
cleanup_and_show "clearance" "clearance emails"
cleanup_and_show "save" "save emails"
cleanup_and_show "percent off" "percent off emails"
cleanup_and_show "free shipping" "free shipping emails"
cleanup_and_show "buy now" "buy now emails"
cleanup_and_show "shop now" "shop now emails"
cleanup_and_show "act now" "act now emails"
cleanup_and_show "don't miss" "don't miss emails"
cleanup_and_show "last chance" "last chance emails"
cleanup_and_show "flash sale" "flash sale emails"
cleanup_and_show "daily deal" "daily deal emails"
cleanup_and_show "weekly special" "weekly special emails"
cleanup_and_show "monthly offer" "monthly offer emails"

# Clean up social media notifications
cleanup_and_show "notification" "notification emails"
cleanup_and_show "like" "like emails"
cleanup_and_show "comment" "comment emails"
cleanup_and_show "follow" "follow emails"
cleanup_and_show "friend request" "friend request emails"
cleanup_and_show "mentioned" "mentioned emails"
cleanup_and_show "tagged" "tagged emails"

# Clean up system notifications
cleanup_and_show "alert" "alert emails"
cleanup_and_show "reminder" "reminder emails"
cleanup_and_show "update" "update emails"
cleanup_and_show "security" "security emails"
cleanup_and_show "password" "password emails"
cleanup_and_show "verification" "verification emails"
cleanup_and_show "confirmation" "confirmation emails"

# Final count
FINAL_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
TOTAL_DELETED=$((CURRENT_COUNT - FINAL_COUNT))

echo "🎉 MEGA CLEANUP COMPLETE!"
echo "========================="
echo "📊 Starting emails: $CURRENT_COUNT"
echo "📊 Final emails: $FINAL_COUNT"
echo "🗑️  Total deleted: $TOTAL_DELETED"
echo ""
echo "💡 Your inbox is now $(( (TOTAL_DELETED * 100) / CURRENT_COUNT ))% cleaner!"
echo ""
echo "🔍 Remaining emails are likely:"
echo "   • Personal emails"
echo "   • Important business emails"
echo "   • Emails you need to keep"
echo ""
echo "✅ Check your Trash folder to review deleted emails!"
