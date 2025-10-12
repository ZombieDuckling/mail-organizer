tell application "Mail"
    activate
    
    -- Get all messages in the inbox
    set inboxMessages to messages of inbox
    set totalMessages to count of inboxMessages
    set readCount to 0
    
    -- Show confirmation dialog
    display dialog "Found " & totalMessages & " messages in inbox. Mark all as read?" buttons {"Cancel", "Mark All Read"} default button "Mark All Read"
    
    if button returned of result is "Mark All Read" then
        -- Mark all messages as read
        repeat with currentMessage in inboxMessages
            try
                set read status of currentMessage to true
                set readCount to readCount + 1
            on error
                -- Skip messages that can't be marked as read
                continue
            end try
        end repeat
        
        -- Show results
        display dialog "Mark as read complete!" & return & return & "Total messages: " & totalMessages & return & "Messages marked as read: " & readCount & return & return & "Unread messages remaining: " & (totalMessages - readCount) buttons {"OK"} default button "OK"
    end if
end tell
