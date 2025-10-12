#!/bin/bash

echo "💥 BULK EMAIL CLEANUP - DELETE BY DATE RANGES"
echo "============================================="
echo ""

CURRENT_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
echo "📊 Starting with: $CURRENT_COUNT emails"
echo ""

# Function to delete emails by date range
delete_by_date() {
    local days="$1"
    local description="$2"
    
    echo "🗑️  Deleting emails older than $description..."
    
    # Create AppleScript to delete old emails
    cat > /tmp/delete_old.scpt << 'SCRIPT_EOF'
tell application "Mail"
    set inboxMessages to messages of inbox
    set deletedCount to 0
    set currentDate to current date
    set cutoffDate to currentDate - (DAYS * days)
    
    repeat with msg in inboxMessages
        try
            set msgDate to date received of msg
            if msgDate < cutoffDate then
                delete msg
                set deletedCount to deletedCount + 1
            end if
        on error
            continue
        end try
    end repeat
    
    return deletedCount
end tell
SCRIPT_EOF
    
    # Replace DAYS placeholder with actual days
    sed "s/DAYS/$days/g" /tmp/delete_old.scpt > /tmp/delete_old_final.scpt
    
    DELETED=$(osascript /tmp/delete_old_final.scpt 2>/dev/null || echo "0")
    echo "   ✅ Deleted $DELETED emails older than $description"
    
    NEW_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    echo "   📊 Remaining: $NEW_COUNT emails"
    echo ""
}

# Delete emails by age
delete_by_date "365" "1 year"
delete_by_date "180" "6 months"
delete_by_date "90" "3 months"
delete_by_date "60" "2 months"
delete_by_date "30" "1 month"
delete_by_date "14" "2 weeks"
delete_by_date "7" "1 week"

# Final count
FINAL_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
TOTAL_DELETED=$((CURRENT_COUNT - FINAL_COUNT))

echo "💥 BULK CLEANUP COMPLETE!"
echo "========================="
echo "📊 Starting emails: $CURRENT_COUNT"
echo "📊 Final emails: $FINAL_COUNT"
echo "🗑️  Total deleted: $TOTAL_DELETED"
echo ""
echo "💡 Your inbox is now $(( (TOTAL_DELETED * 100) / CURRENT_COUNT ))% cleaner!"
echo ""
echo "⚠️  WARNING: This deleted emails by age!"
echo "   Check your Trash folder to review deleted emails!"
