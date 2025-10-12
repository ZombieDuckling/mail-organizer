tell application "Mail"
    set inboxMessages to messages of inbox
    set totalCount to count of inboxMessages
    set promotionalCount to 0
    set socialCount to 0
    set notificationCount to 0
    set oldCount to 0
    set senderList to {}
    
    -- Get current date for age comparison
    set currentDate to current date
    
    repeat with msg in inboxMessages
        try
            set msgSubject to subject of msg
            set msgSender to sender of msg
            set msgDate to date received of msg
            set daysOld to (currentDate - msgDate) / days
            
            -- Count promotional emails
            if msgSubject contains "promotional" or msgSubject contains "marketing" or msgSubject contains "newsletter" or msgSubject contains "offers" or msgSubject contains "sale" or msgSubject contains "discount" or msgSubject contains "deal" or msgSubject contains "unsubscribe" or msgSubject contains "limited time" or msgSubject contains "exclusive" or msgSubject contains "special offer" or msgSubject contains "clearance" or msgSubject contains "save" or msgSubject contains "percent off" or msgSubject contains "free shipping" or msgSubject contains "buy now" or msgSubject contains "shop now" or msgSubject contains "act now" or msgSubject contains "don't miss" or msgSubject contains "last chance" or msgSubject contains "flash sale" or msgSubject contains "daily deal" or msgSubject contains "weekly special" or msgSubject contains "monthly offer" then
                set promotionalCount to promotionalCount + 1
            end if
            
            -- Count social media notifications
            if msgSubject contains "notification" or msgSubject contains "like" or msgSubject contains "comment" or msgSubject contains "follow" or msgSubject contains "friend request" or msgSubject contains "mentioned" or msgSubject contains "tagged" then
                set socialCount to socialCount + 1
            end if
            
            -- Count system notifications
            if msgSubject contains "alert" or msgSubject contains "reminder" or msgSubject contains "update" or msgSubject contains "security" or msgSubject contains "password" or msgSubject contains "verification" or msgSubject contains "confirmation" then
                set notificationCount to notificationCount + 1
            end if
            
            -- Count old emails (older than 30 days)
            if daysOld > 30 then
                set oldCount to oldCount + 1
            end if
            
            -- Track senders
            set end of senderList to msgSender
            
        on error
            continue
        end try
    end repeat
    
    -- Create report
    set reportMessage to "📊 INBOX ANALYSIS REPORT" & return & return & "Total emails: " & totalCount & return & return & "📧 Promotional emails: " & promotionalCount & return & "📱 Social notifications: " & socialCount & return & "🔔 System notifications: " & notificationCount & return & "📅 Old emails (>30 days): " & oldCount & return & return & "🎯 RECOMMENDATIONS:" & return & "• Delete " & promotionalCount & " promotional emails" & return & "• Delete " & socialCount & " social notifications" & return & "• Review " & notificationCount & " system notifications" & return & "• Archive " & oldCount & " old emails"
    
    display dialog reportMessage buttons {"OK", "Start Cleanup"} default button "Start Cleanup"
    
    if button returned of result is "Start Cleanup" then
        return "start_cleanup"
    else
        return "analysis_only"
    end if
end tell
