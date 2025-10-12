tell application "Mail"
    set inboxMessages to messages of inbox
    set promotionalCount to 0
    set deletedCount to 0
    
    repeat with currentMessage in inboxMessages
        try
            set messageSubject to subject of currentMessage
            set messageSender to sender of currentMessage
            set isPromotional to false
            
            if messageSubject contains "unsubscribe" then
                set isPromotional to true
            else if messageSubject contains "promotional" then
                set isPromotional to true
            else if messageSubject contains "marketing" then
                set isPromotional to true
            else if messageSubject contains "newsletter" then
                set isPromotional to true
            else if messageSubject contains "offers" then
                set isPromotional to true
            else if messageSubject contains "sale" then
                set isPromotional to true
            else if messageSubject contains "discount" then
                set isPromotional to true
            else if messageSubject contains "deal" then
                set isPromotional to true
            end if
            
            if messageSender contains "noreply" then
                set isPromotional to true
            else if messageSender contains "no-reply" then
                set isPromotional to true
            else if messageSender contains "marketing" then
                set isPromotional to true
            else if messageSender contains "promo" then
                set isPromotional to true
            else if messageSender contains "offers" then
                set isPromotional to true
            else if messageSender contains "deals" then
                set isPromotional to true
            else if messageSender contains "newsletter" then
                set isPromotional to true
            else if messageSender contains "notifications" then
                set isPromotional to true
            end if
            
            if isPromotional then
                set promotionalCount to promotionalCount + 1
                move currentMessage to trash
                set deletedCount to deletedCount + 1
            end if
            
        on error
            continue
        end try
    end repeat
    
    display dialog "Organization complete! Promotional emails found: " & promotionalCount & " Emails moved to trash: " & deletedCount buttons {"OK"} default button "OK"
end tell
