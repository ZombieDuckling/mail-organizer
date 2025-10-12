tell application "Mail"
    set inboxMessages to messages of inbox
    set deletedCount to 0
    
    repeat with msg in inboxMessages
        try
            if subject of msg contains "newsletter" then
                delete msg
                set deletedCount to deletedCount + 1
            end if
        on error
            continue
        end try
    end repeat
    
    display dialog "Deleted " & deletedCount & " newsletter emails" buttons {"OK"}
end tell
