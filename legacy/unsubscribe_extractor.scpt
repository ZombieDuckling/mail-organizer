tell application "Mail"
    set inboxMessages to messages of inbox
    set unsubscribeCount to 0
    set unsubscribeLinks to {}
    set unsubscribeSenders to {}
    
    repeat with msg in inboxMessages
        try
            set msgContent to content of msg
            set msgSender to sender of msg
            
            -- Look for unsubscribe links in the content
            if msgContent contains "unsubscribe" then
                set unsubscribeCount to unsubscribeCount + 1
                set end of unsubscribeSenders to msgSender
                
                -- Try to extract unsubscribe URL (basic pattern matching)
                set contentLines to paragraphs of msgContent
                repeat with line in contentLines
                    if line contains "unsubscribe" and line contains "http" then
                        set end of unsubscribeLinks to line
                        exit repeat
                    end if
                end repeat
            end if
            
        on error
            continue
        end try
    end repeat
    
    -- Create report
    set reportMessage to "Unsubscribe Analysis Complete!" & return & return & "Found " & unsubscribeCount & " emails with unsubscribe links" & return & return
    
    if unsubscribeCount > 0 then
        set reportMessage to reportMessage & "Senders with unsubscribe links:" & return
        repeat with i from 1 to count of unsubscribeSenders
            set reportMessage to reportMessage & i & ". " & item i of unsubscribeSenders & return
        end repeat
        
        if count of unsubscribeLinks > 0 then
            set reportMessage to reportMessage & return & "Sample unsubscribe links found:" & return
            repeat with i from 1 to (count of unsubscribeLinks)
                if i ≤ 5 then -- Show first 5 links
                    set reportMessage to reportMessage & "• " & item i of unsubscribeLinks & return
                end if
            end repeat
        end if
    end if
    
    display dialog reportMessage buttons {"OK", "Save Report"} default button "OK"
    
    if button returned of result is "Save Report" then
        -- Save report to file
        set reportFile to (path to desktop as string) & "unsubscribe_report.txt"
        set fileRef to open for access file reportFile with write permission
        write reportMessage to fileRef
        close access fileRef
        display dialog "Report saved to Desktop as unsubscribe_report.txt" buttons {"OK"}
    end if
end tell
