tell application "Mail"
    set inboxMessages to messages of inbox
    set deletedCount to 0
    set unsubscribeCount to 0
    set unsubscribeList to {}
    
    repeat with msg in inboxMessages
        try
            set msgSubject to subject of msg
            set msgSender to sender of msg
            set msgContent to content of msg
            set isPromo to false
            set hasUnsubscribe to false
            
            -- Check for promotional keywords in subject
            if msgSubject contains "promotional" or msgSubject contains "marketing" or msgSubject contains "newsletter" or msgSubject contains "offers" or msgSubject contains "sale" or msgSubject contains "discount" or msgSubject contains "deal" or msgSubject contains "unsubscribe" then
                set isPromo to true
            else if msgSender contains "noreply" or msgSender contains "no-reply" or msgSender contains "marketing" or msgSender contains "promo" or msgSender contains "offers" or msgSender contains "deals" or msgSender contains "newsletter" or msgSender contains "notifications" then
                set isPromo to true
            end if
            
            -- Check for unsubscribe links in content
            if msgContent contains "unsubscribe" then
                set hasUnsubscribe to true
                set isPromo to true
            end if
            
            if isPromo then
                if hasUnsubscribe then
                    -- Add to unsubscribe list instead of deleting
                    set unsubscribeCount to unsubscribeCount + 1
                    set end of unsubscribeList to msgSender
                else
                    -- Delete emails without unsubscribe links
                    delete msg
                    set deletedCount to deletedCount + 1
                end if
            end if
            
        on error
            continue
        end try
    end repeat
    
    -- Show results
    set resultMessage to "Email organization complete!" & return & return & "Deleted emails: " & deletedCount & return & "Emails with unsubscribe links found: " & unsubscribeCount
    
    if unsubscribeCount > 0 then
        set resultMessage to resultMessage & return & return & "Unsubscribe links found from these senders:" & return
        repeat with sender in unsubscribeList
            set resultMessage to resultMessage & "• " & sender & return
        end repeat
        set resultMessage to resultMessage & return & "You can manually unsubscribe from these senders."
    end if
    
    display dialog resultMessage buttons {"OK"} default button "OK"
end tell
