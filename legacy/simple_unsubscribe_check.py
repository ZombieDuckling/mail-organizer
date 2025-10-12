#!/usr/bin/env python3
"""
Simple Unsubscribe Checker
"""

import subprocess
import re

def check_unsubscribe_emails():
    """Check for emails with unsubscribe links"""
    print("🔍 Checking for emails with unsubscribe links...")
    
    # Simple AppleScript to count emails with unsubscribe
    script = '''
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
        
        return unsubscribeCount
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            count = result.stdout.strip()
            print(f"📊 Found {count} emails with unsubscribe links")
            
            if int(count) > 0:
                print("\n💡 These emails contain unsubscribe links:")
                print("   You can manually unsubscribe from these senders")
                print("   or use the smart cleanup option to preserve them")
                
                # Ask what to do
                print(f"\n🤔 What would you like to do?")
                print("1. Delete all promotional emails (including unsubscribe ones)")
                print("2. Keep emails with unsubscribe links for manual review")
                print("3. Do nothing")
                
                choice = input("Enter your choice (1-3): ").strip()
                
                if choice == "1":
                    delete_promotional_emails()
                elif choice == "2":
                    smart_cleanup()
                else:
                    print("No action taken.")
            else:
                print("✅ No emails with unsubscribe links found!")
        else:
            print(f"❌ Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Script timed out. Your inbox might be very large.")
    except Exception as e:
        print(f"❌ Error: {e}")

def delete_promotional_emails():
    """Delete all promotional emails"""
    print("\n🗑️  Deleting all promotional emails...")
    
    script = '''
    tell application "Mail"
        set inboxMessages to messages of inbox
        set deletedCount to 0
        
        repeat with msg in inboxMessages
            try
                set msgSubject to subject of msg
                set msgSender to sender of msg
                set isPromo to false
                
                if msgSubject contains "promotional" or msgSubject contains "marketing" or msgSubject contains "newsletter" or msgSubject contains "offers" or msgSubject contains "sale" or msgSubject contains "discount" or msgSubject contains "deal" or msgSubject contains "unsubscribe" then
                    set isPromo to true
                else if msgSender contains "noreply" or msgSender contains "no-reply" or msgSender contains "marketing" or msgSender contains "promo" or msgSender contains "offers" or msgSender contains "deals" or msgSender contains "newsletter" or msgSender contains "notifications" then
                    set isPromo to true
                end if
                
                if isPromo then
                    delete msg
                    set deletedCount to deletedCount + 1
                end if
            on error
                continue
            end try
        end repeat
        
        return deletedCount
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            deleted_count = result.stdout.strip()
            print(f"✅ Deleted {deleted_count} promotional emails!")
        else:
            print(f"❌ Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Deletion timed out. Some emails may have been deleted.")
    except Exception as e:
        print(f"❌ Error: {e}")

def smart_cleanup():
    """Smart cleanup that preserves unsubscribe emails"""
    print("\n🧠 Running smart cleanup (preserving unsubscribe emails)...")
    
    script = '''
    tell application "Mail"
        set inboxMessages to messages of inbox
        set deletedCount to 0
        set preservedCount to 0
        
        repeat with msg in inboxMessages
            try
                set msgSubject to subject of msg
                set msgSender to sender of msg
                set msgContent to content of msg
                set isPromo to false
                set hasUnsubscribe to false
                
                if msgSubject contains "promotional" or msgSubject contains "marketing" or msgSubject contains "newsletter" or msgSubject contains "offers" or msgSubject contains "sale" or msgSubject contains "discount" or msgSubject contains "deal" then
                    set isPromo to true
                else if msgSender contains "noreply" or msgSender contains "no-reply" or msgSender contains "marketing" or msgSender contains "promo" or msgSender contains "offers" or msgSender contains "deals" or msgSender contains "newsletter" or msgSender contains "notifications" then
                    set isPromo to true
                end if
                
                if msgContent contains "unsubscribe" then
                    set hasUnsubscribe to true
                end if
                
                if isPromo then
                    if hasUnsubscribe then
                        set preservedCount to preservedCount + 1
                    else
                        delete msg
                        set deletedCount to deletedCount + 1
                    end if
                end if
            on error
                continue
            end try
        end repeat
        
        return deletedCount & "|" & preservedCount
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            counts = result.stdout.strip().split('|')
            deleted_count = counts[0] if len(counts) > 0 else "0"
            preserved_count = counts[1] if len(counts) > 1 else "0"
            print(f"✅ Smart cleanup complete!")
            print(f"   Deleted: {deleted_count} promotional emails")
            print(f"   Preserved: {preserved_count} emails with unsubscribe links")
        else:
            print(f"❌ Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Smart cleanup timed out. Some emails may have been processed.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_unsubscribe_emails()
