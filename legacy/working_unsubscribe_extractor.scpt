tell application "Mail"
    set inboxMessages to messages of inbox
    set unsubscribeCount to 0
    set unsubscribeSenders to {}
    
    repeat with msg in inboxMessages
        try
            set msgContent to content of msg
            set msgSender to sender of msg
            
            if msgContent contains "unsubscribe" then
                set unsubscribeCount to unsubscribeCount + 1
                set end of unsubscribeSenders to msgSender
            end if
            
        on error
            continue
        end try
    end repeat
    
    set reportMessage to "Unsubscribe Analysis Complete!" & return & return & "Found " & unsubscribeCount & " emails with unsubscribe links" & return & return
    
    if unsubscribeCount > 0 then
        set reportMessage to reportMessage & "Senders with unsubscribe links:" & return
        repeat with i from 1 to count of unsubscribeSenders
            set reportMessage to reportMessage & i & ". " & item i of unsubscribeSenders & return
        end repeat
    end if
    
    display dialog reportMessage buttons {"OK", "Save Report"} default button "OK"
    
    if button returned of result is "Save Report" then
        set reportFile to (path to desktop as string) & "unsubscribe_report.txt"
        set fileRef to open for access file reportFile with write permission
        write reportMessage to fileRef
        close access fileRef
        display dialog "Report saved to Desktop as unsubscribe_report.txt" buttons {"OK"}
    end if
end tell
