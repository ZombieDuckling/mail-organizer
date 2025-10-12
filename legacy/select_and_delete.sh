#!/bin/bash

echo "🎯 SELECT AND DELETE EMAILS IN MAIL"
echo "==================================="
echo ""

CURRENT_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
echo "📊 Starting with: $CURRENT_COUNT emails"
echo ""

# Function to select and delete emails
select_and_delete() {
    local count="$1"
    local description="$2"
    
    echo "🎯 Selecting $description..."
    
    # Create AppleScript to select and delete emails
    cat > /tmp/select_delete.scpt << 'SCRIPT_EOF'
tell application "Mail"
    activate
    set inboxMessages to messages of inbox
    set selectedCount to 0
    
    -- Select first COUNT emails
    repeat with i from 1 to COUNT
        try
            if i ≤ (count of inboxMessages) then
                set msg to item i of inboxMessages
                select msg
                set selectedCount to selectedCount + 1
            end if
        on error
            continue
        end try
    end repeat
    
    -- Delete selected emails
    if selectedCount > 0 then
        delete selected messages
    end if
    
    return selectedCount
end tell
SCRIPT_EOF
    
    # Replace COUNT placeholder
    sed "s/COUNT/$count/g" /tmp/select_delete.scpt > /tmp/select_delete_final.scpt
    
    DELETED=$(osascript /tmp/select_delete_final.scpt 2>/dev/null || echo "0")
    echo "   ✅ Deleted $DELETED emails"
    
    NEW_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    echo "   📊 Remaining: $NEW_COUNT emails"
    echo ""
}

# Ask user for confirmation
echo "⚠️  WARNING: This will select and delete emails in Mail!"
echo "   Make sure Mail is open and visible!"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    # Select and delete in batches
    select_and_delete "100" "first 100 emails"
    select_and_delete "100" "next 100 emails"
    select_and_delete "100" "next 100 emails"
    select_and_delete "100" "next 100 emails"
    select_and_delete "100" "next 100 emails"
    
    # Final count
    FINAL_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    TOTAL_DELETED=$((CURRENT_COUNT - FINAL_COUNT))
    
    echo "🎯 SELECT AND DELETE COMPLETE!"
    echo "==============================="
    echo "📊 Starting emails: $CURRENT_COUNT"
    echo "📊 Final emails: $FINAL_COUNT"
    echo "🗑️  Total deleted: $TOTAL_DELETED"
    echo ""
    echo "💡 Your inbox is now $(( (TOTAL_DELETED * 100) / CURRENT_COUNT ))% cleaner!"
else
    echo "❌ Select and delete cancelled."
fi
