-- Create Mail Rules for Automatic Organization
-- This script creates rules to automatically handle promotional emails

tell application "Mail"
    activate
    
    -- Create a rule for promotional emails
    set newRule to make new rule with properties {name:"Auto-Delete Promotional Emails", enabled:true}
    
    -- Add conditions for the rule
    set condition1 to make new rule condition with properties {rule type:subject contains value, expression:"unsubscribe"}
    set condition2 to make new new rule condition with properties {rule type:subject contains value, expression:"promotional"}
    set condition3 to make new rule condition with properties {rule type:subject contains value, expression:"marketing"}
    set condition4 to make new rule condition with properties {rule type:subject contains value, expression:"newsletter"}
    set condition5 to make new rule condition with properties {rule type:subject contains value, expression:"offers"}
    set condition6 to make new rule condition with properties {rule type:subject contains value, expression:"sale"}
    set condition7 to make new rule condition with properties {rule type:subject contains value, expression:"discount"}
    set condition8 to make new rule condition with properties {rule type:subject contains value, expression:"deal"}
    
    -- Add action to move to trash
    set action1 to make new rule action with properties {rule type:move message, destination:trash mailbox}
    
    display dialog "Mail rules created successfully!" & return & return & "The following rule has been added:" & return & "• Auto-Delete Promotional Emails" & return & return & "This rule will automatically move promotional emails to trash." buttons {"OK"} default button "OK"
end tell
