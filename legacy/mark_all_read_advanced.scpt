tell application "Mail"
    activate
    
    -- Get all messages in the inbox
    set inboxMessages to messages of inbox
    set totalMessages to count of inboxMessages
    set readCount to 0
    
    -- Show confirmation dialog with options
    set dialogResult to display dialog "Found " & totalMessages & " messages in inbox. What would you like to do?" buttons {"Cancel", "Inbox Only", "All Mailboxes"} default button "Inbox Only"
    
    if button returned of dialogResult is "Inbox Only" then
        -- Mark only inbox messages as read
        repeat with currentMessage in inboxMessages
            try
                set read status of currentMessage to true
                set readCount to readCount + 1
            on error
                continue
            end try
        end repeat
        
        display dialog "Inbox mark as read complete!" & return & return & "Total inbox messages: " & totalMessages & return & "Messages marked as read: " & readCount & return & return & "Unread messages remaining: " & (totalMessages - readCount) buttons {"OK"} default button "OK"
        
    else if button returned of dialogResult is "All Mailboxes" then
        -- Mark all messages in all mailboxes as read
        set allMailboxes to every mailbox
        set totalAllMessages to 0
        set totalReadCount to 0
        
        repeat with currentMailbox in allMailboxes
            try
                set mailboxMessages to messages of currentMailbox
                set mailboxCount to count of mailboxMessages
                set totalAllMessages to totalAllMessages + mailboxCount
                
                repeat with currentMessage in mailboxMessages
                    try
                        set read status of currentMessage to true
                        set totalReadCount to totalReadCount + 1
                    on error
                        continue
                    end try
                end repeat
            on error
                continue
            end try
        end repeat
        
        display dialog "All mailboxes mark as read complete!" & return & return & "Total messages in all mailboxes: " & totalAllMessages & return & "Messages marked as read: " & totalReadCount & return & return & "Unread messages remaining: " & (totalAllMessages - totalReadCount) buttons {"OK"} default button "OK"
    end if
end tell
