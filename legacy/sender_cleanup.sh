#!/bin/bash

echo "🎯 AGGRESSIVE SENDER-BASED CLEANUP"
echo "=================================="
echo ""

CURRENT_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
echo "📊 Starting with: $CURRENT_COUNT emails"
echo ""

# Function to clean by sender domain
cleanup_sender() {
    local sender="$1"
    local description="$2"
    
    echo "🧹 Cleaning emails from $description..."
    
    osascript -e "tell application \"Mail\"" -e "set inboxMessages to messages of inbox" -e "set deletedCount to 0" -e "repeat with msg in inboxMessages" -e "try" -e "if sender of msg contains \"$sender\" then" -e "delete msg" -e "set deletedCount to deletedCount + 1" -e "end if" -e "on error" -e "continue" -e "end try" -e "end repeat" -e "return deletedCount" -e "end tell" > /tmp/sender_deleted.txt 2>/dev/null
    
    DELETED=$(cat /tmp/sender_deleted.txt 2>/dev/null || echo "0")
    echo "   ✅ Deleted $DELETED emails from $description"
    
    NEW_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
    echo "   📊 Remaining: $NEW_COUNT emails"
    echo ""
}

# Clean up common promotional domains
cleanup_sender "noreply" "noreply senders"
cleanup_sender "no-reply" "no-reply senders"
cleanup_sender "marketing" "marketing senders"
cleanup_sender "promo" "promo senders"
cleanup_sender "offers" "offers senders"
cleanup_sender "deals" "deals senders"
cleanup_sender "newsletter" "newsletter senders"
cleanup_sender "notifications" "notifications senders"
cleanup_sender "alerts" "alerts senders"
cleanup_sender "updates" "updates senders"
cleanup_sender "digest" "digest senders"
cleanup_sender "mailing" "mailing senders"
cleanup_sender "subscription" "subscription senders"
cleanup_sender "unsubscribe" "unsubscribe senders"

# Clean up common promotional companies
cleanup_sender "amazon" "Amazon promotional"
cleanup_sender "ebay" "eBay promotional"
cleanup_sender "etsy" "Etsy promotional"
cleanup_sender "shopify" "Shopify promotional"
cleanup_sender "mailchimp" "MailChimp promotional"
cleanup_sender "constant" "Constant Contact"
cleanup_sender "aweber" "AWeber promotional"
cleanup_sender "getresponse" "GetResponse promotional"
cleanup_sender "convertkit" "ConvertKit promotional"
cleanup_sender "activecampaign" "ActiveCampaign promotional"

# Clean up social media notifications
cleanup_sender "facebook" "Facebook notifications"
cleanup_sender "twitter" "Twitter notifications"
cleanup_sender "instagram" "Instagram notifications"
cleanup_sender "linkedin" "LinkedIn notifications"
cleanup_sender "pinterest" "Pinterest notifications"
cleanup_sender "tiktok" "TikTok notifications"
cleanup_sender "snapchat" "Snapchat notifications"
cleanup_sender "youtube" "YouTube notifications"

# Clean up common promotional services
cleanup_sender "groupon" "Groupon"
cleanup_sender "livingsocial" "LivingSocial"
cleanup_sender "retailmenot" "RetailMeNot"
cleanup_sender "honey" "Honey"
cleanup_sender "rakuten" "Rakuten"
cleanup_sender "ebates" "Ebates"
cleanup_sender "ibotta" "Ibotta"
cleanup_sender "fetch" "Fetch Rewards"
cleanup_sender "swagbucks" "Swagbucks"

# Final count
FINAL_COUNT=$(osascript -e 'tell application "Mail" to return count of messages of inbox')
TOTAL_DELETED=$((CURRENT_COUNT - FINAL_COUNT))

echo "🎉 SENDER CLEANUP COMPLETE!"
echo "============================"
echo "📊 Starting emails: $CURRENT_COUNT"
echo "📊 Final emails: $FINAL_COUNT"
echo "🗑️  Total deleted: $TOTAL_DELETED"
echo ""
echo "💡 Your inbox is now $(( (TOTAL_DELETED * 100) / CURRENT_COUNT ))% cleaner!"
