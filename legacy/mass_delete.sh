#!/bin/bash

echo "💥 MASS EMAIL DELETION - NUCLEAR OPTION"
echo "======================================="
echo ""

CURRENT_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
echo "📊 Starting with: $CURRENT_COUNT emails"
echo ""

# Function to delete emails in batches
delete_batch() {
    local batch_size="$1"
    local description="$2"
    
    echo "🗑️  Deleting $description..."
    
    # Create AppleScript to delete a batch of emails
    cat > /tmp/delete_batch.scpt << 'SCRIPT_EOF'
tell application "Mail"
    set inboxMessages to messages of inbox
    set deletedCount to 0
    set batchSize to BATCH_SIZE
    
    repeat with i from 1 to batchSize
        try
            if i ≤ (count of inboxMessages) then
                set msg to item i of inboxMessages
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
    
    # Replace BATCH_SIZE placeholder
    sed "s/BATCH_SIZE/$batch_size/g" /tmp/delete_batch.scpt > /tmp/delete_batch_final.scpt
    
    DELETED=$(osascript /tmp/delete_batch_final.scpt 2>/dev/null || echo "0")
    echo "   ✅ Deleted $DELETED emails"
    
    NEW_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    echo "   📊 Remaining: $NEW_COUNT emails"
    echo ""
}

# Ask user for confirmation
echo "⚠️  WARNING: This will delete emails in large batches!"
echo "   This is a NUCLEAR option - use with caution!"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    # Delete in batches
    delete_batch "1000" "first 1000 emails"
    delete_batch "1000" "next 1000 emails"
    delete_batch "1000" "next 1000 emails"
    delete_batch "1000" "next 1000 emails"
    delete_batch "1000" "next 1000 emails"
    delete_batch "1000" "next 1000 emails"
    delete_batch "1000" "next 1000 emails"
    delete_batch "1000" "next 1000 emails"
    delete_batch "1000" "next 1000 emails"
    delete_batch "1000" "next 1000 emails"
    
    # Final count
    FINAL_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    TOTAL_DELETED=$((CURRENT_COUNT - FINAL_COUNT))
    
    echo "💥 MASS DELETION COMPLETE!"
    echo "=========================="
    echo "📊 Starting emails: $CURRENT_COUNT"
    echo "📊 Final emails: $FINAL_COUNT"
    echo "🗑️  Total deleted: $TOTAL_DELETED"
    echo ""
    echo "💡 Your inbox is now $(( (TOTAL_DELETED * 100) / CURRENT_COUNT ))% cleaner!"
    echo ""
    echo "⚠️  WARNING: This was a MASS DELETION!"
    echo "   Check your Trash folder to review deleted emails!"
else
    echo "❌ Mass deletion cancelled."
fi
