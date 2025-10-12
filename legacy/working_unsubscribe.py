#!/usr/bin/env python3
import subprocess

def check_unsubscribe():
    print("🔍 Checking for emails with unsubscribe links...")
    
    # Simple count check
    script = 'tell application "Mail" to return count of messages of inbox'
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    
    if result.returncode == 0:
        total = result.stdout.strip()
        print(f"📊 Total emails in inbox: {total}")
        
        # Ask what to do
        print(f"\n🤔 What would you like to do?")
        print("1. Delete all promotional emails")
        print("2. Smart cleanup (preserve unsubscribe emails)")
        print("3. Do nothing")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            delete_promotional()
        elif choice == "2":
            smart_cleanup()
        else:
            print("No action taken.")
    else:
        print(f"❌ Error: {result.stderr}")

def delete_promotional():
    print("\n🗑️  Deleting promotional emails...")
    script = '''
    tell application "Mail"
        set inboxMessages to messages of inbox
        set deletedCount to 0
        repeat with msg in inboxMessages
            try
                set msgSubject to subject of msg
                set msgSender to sender of msg
                set isPromo to false
                if msgSubject contains "unsubscribe" or msgSubject contains "promotional" or msgSubject contains "marketing" or msgSubject contains "newsletter" or msgSubject contains "offers" or msgSubject contains "sale" or msgSubject contains "discount" or msgSubject contains "deal" then
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
    
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    if result.returncode == 0:
        deleted = result.stdout.strip()
        print(f"✅ Deleted {deleted} promotional emails!")
    else:
        print(f"❌ Error: {result.stderr}")

def smart_cleanup():
    print("\n🧠 Smart cleanup (preserving unsubscribe emails)...")
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
    
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    if result.returncode == 0:
        counts = result.stdout.strip().split('|')
        deleted = counts[0] if len(counts) > 0 else "0"
        preserved = counts[1] if len(counts) > 1 else "0"
        print(f"✅ Smart cleanup complete!")
        print(f"   Deleted: {deleted} promotional emails")
        print(f"   Preserved: {preserved} emails with unsubscribe links")
    else:
        print(f"❌ Error: {result.stderr}")

if __name__ == "__main__":
    check_unsubscribe()
