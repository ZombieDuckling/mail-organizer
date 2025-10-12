tell application "Mail"
    activate
    
    set inboxMessages to messages of inbox
    set totalMessages to count of inboxMessages
    display dialog "Found " & totalMessages & " messages in inbox. Continue with organization?" buttons {"Cancel", "Continue"} default button "Continue"
    
    if button returned of result is "Continue" then
        set promotionalCount to 0
        set deletedCount to 0
        
        repeat with currentMessage in inboxMessages
            try
                set messageSubject to subject of currentMessage
                set messageSender to sender of currentMessage
                set messageContent to content of currentMessage
                set isPromotional to false
                
                set promotionalKeywords to {"unsubscribe", "promotional", "marketing", "newsletter", "offers", "sale", "discount", "deal", "limited time", "exclusive", "special offer", "clearance", "save", "percent off", "free shipping", "buy now", "shop now", "act now", "don't miss", "last chance", "flash sale", "daily deal", "weekly special", "monthly offer"}
                
                repeat with keyword in promotionalKeywords
                    if messageSubject contains keyword then
                        set isPromotional to true
                        exit repeat
                    end if
                end repeat
                
                set promotionalDomains to {"noreply", "no-reply", "marketing", "promo", "offers", "deals", "newsletter", "notifications", "alerts", "updates", "digest"}
                
                repeat with domain in promotionalDomains
                    if messageSender contains domain then
                        set isPromotional to true
                        exit repeat
                    end if
                end repeat
                
                if messageContent contains "unsubscribe" then
                    set isPromotional to true
                end if
                
                if isPromotional then
                    set promotionalCount to promotionalCount + 1
                    move currentMessage to trash
                    set deletedCount to deletedCount + 1
                end if
                
            on error errorMessage
                continue
            end try
        end repeat
        
        display dialog "Organization complete!" & return & return & "Promotional emails found: " & promotionalCount & return & "Emails moved to trash: " & deletedCount & return & return & "Remaining emails: " & (totalMessages - deletedCount) buttons {"OK"} default button "OK"
        
    end if
end tell
