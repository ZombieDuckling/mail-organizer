#!/bin/bash

echo "💥 NUCLEAR EMAIL CLEANUP - MAXIMUM AGGRESSION"
echo "============================================="
echo ""

CURRENT_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
echo "📊 Starting with: $CURRENT_COUNT emails"
echo ""

# Function to clean by age
cleanup_old_emails() {
    local days="$1"
    local description="$2"
    
    echo "🧹 Cleaning emails older than $description..."
    
    osascript -e "tell application \"Mail\"" -e "set inboxMessages to messages of inbox" -e "set deletedCount to 0" -e "set currentDate to current date" -e "repeat with msg in inboxMessages" -e "try" -e "set msgDate to date received of msg" -e "set daysOld to (currentDate - msgDate) / days" -e "if daysOld > $days then" -e "delete msg" -e "set deletedCount to deletedCount + 1" -e "end if" -e "on error" -e "continue" -e "end try" -e "end repeat" -e "return deletedCount" -e "end tell" > /tmp/age_deleted.txt 2>/dev/null
    
    DELETED=$(cat /tmp/age_deleted.txt 2>/dev/null || echo "0")
    echo "   ✅ Deleted $DELETED emails older than $description"
    
    NEW_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    echo "   📊 Remaining: $NEW_COUNT emails"
    echo ""
}

# Clean up very old emails
cleanup_old_emails "365" "1 year"
cleanup_old_emails "180" "6 months"
cleanup_old_emails "90" "3 months"
cleanup_old_emails "30" "1 month"

# Function to clean by content patterns
cleanup_content() {
    local pattern="$1"
    local description="$2"
    
    echo "🧹 Cleaning emails with $description..."
    
    osascript -e "tell application \"Mail\"" -e "set inboxMessages to messages of inbox" -e "set deletedCount to 0" -e "repeat with msg in inboxMessages" -e "try" -e "set msgContent to content of msg" -e "if msgContent contains \"$pattern\" then" -e "delete msg" -e "set deletedCount to deletedCount + 1" -e "end if" -e "on error" -e "continue" -e "end try" -e "end repeat" -e "return deletedCount" -e "end tell" > /tmp/content_deleted.txt 2>/dev/null
    
    DELETED=$(cat /tmp/content_deleted.txt 2>/dev/null || echo "0")
    echo "   ✅ Deleted $DELETED emails with $description"
    
    NEW_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    echo "   📊 Remaining: $NEW_COUNT emails"
    echo ""
}

# Clean up by content patterns
cleanup_content "unsubscribe" "unsubscribe links"
cleanup_content "click here" "click here links"
cleanup_content "view in browser" "view in browser links"
cleanup_content "privacy policy" "privacy policy links"
cleanup_content "terms of service" "terms of service links"
cleanup_content "opt out" "opt out links"
cleanup_content "manage preferences" "manage preferences links"
cleanup_content "update preferences" "update preferences links"
cleanup_content "change email" "change email links"
cleanup_content "unsubscribe from" "unsubscribe from links"

# Function to clean by attachment patterns
cleanup_attachments() {
    local description="$1"
    
    echo "🧹 Cleaning emails with $description..."
    
    osascript -e "tell application \"Mail\"" -e "set inboxMessages to messages of inbox" -e "set deletedCount to 0" -e "repeat with msg in inboxMessages" -e "try" -e "if (count of mail attachments of msg) > 0 then" -e "delete msg" -e "set deletedCount to deletedCount + 1" -e "end if" -e "on error" -e "continue" -e "end try" -e "end repeat" -e "return deletedCount" -e "end tell" > /tmp/attachment_deleted.txt 2>/dev/null
    
    DELETED=$(cat /tmp/attachment_deleted.txt 2>/dev/null || echo "0")
    echo "   ✅ Deleted $DELETED emails with $description"
    
    NEW_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    echo "   📊 Remaining: $NEW_COUNT emails"
    echo ""
}

# Clean up emails with attachments (often promotional)
cleanup_attachments "attachments"

# Final count
FINAL_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
TOTAL_DELETED=$((CURRENT_COUNT - FINAL_COUNT))

echo "💥 NUCLEAR CLEANUP COMPLETE!"
echo "============================="
echo "📊 Starting emails: $CURRENT_COUNT"
echo "📊 Final emails: $FINAL_COUNT"
echo "🗑️  Total deleted: $TOTAL_DELETED"
echo ""
echo "💡 Your inbox is now $(( (TOTAL_DELETED * 100) / CURRENT_COUNT ))% cleaner!"
echo ""
echo "🔍 Remaining emails are likely:"
echo "   • Recent personal emails"
echo "   • Important business emails"
echo "   • Emails without promotional content"
echo ""
echo "⚠️  WARNING: This was an aggressive cleanup!"
echo "   Check your Trash folder to review deleted emails!"
