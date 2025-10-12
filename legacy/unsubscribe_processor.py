#!/usr/bin/env python3
"""
Advanced Email Unsubscribe Processor
This script can extract unsubscribe links and optionally process them
"""

import re
import osascript
import webbrowser
import time
from urllib.parse import urlparse

def get_emails_with_unsubscribe():
    """Get emails with unsubscribe links using AppleScript"""
    script = '''
    tell application "Mail"
        set inboxMessages to messages of inbox
        set unsubscribeEmails to {}
        
        repeat with msg in inboxMessages
            try
                set msgContent to content of msg
                set msgSender to sender of msg
                set msgSubject to subject of msg
                
                if msgContent contains "unsubscribe" then
                    set end of unsubscribeEmails to msgSender & "|" & msgSubject & "|" & msgContent
                end if
            on error
                continue
            end try
        end repeat
        
        return unsubscribeEmails
    end tell
    '''
    
    result = osascript.run(script)
    return result.out.split(',') if result.out else []

def extract_unsubscribe_links(content):
    """Extract unsubscribe links from email content"""
    # Common unsubscribe link patterns
    patterns = [
        r'href=["\']([^"\']*unsubscribe[^"\']*)["\']',
        r'https?://[^\s]*unsubscribe[^\s]*',
        r'<a[^>]*href=["\']([^"\']*unsubscribe[^"\']*)["\'][^>]*>',
        r'mailto:[^\s]*unsubscribe[^\s]*'
    ]
    
    links = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        links.extend(matches)
    
    return list(set(links))  # Remove duplicates

def is_safe_unsubscribe_url(url):
    """Check if unsubscribe URL is safe to process"""
    try:
        parsed = urlparse(url)
        # Only allow http/https and mailto
        return parsed.scheme in ['http', 'https', 'mailto']
    except:
        return False

def process_unsubscribe_links():
    """Main function to process unsubscribe links"""
    print("🔍 Scanning emails for unsubscribe links...")
    
    emails = get_emails_with_unsubscribe()
    print(f"Found {len(emails)} emails with unsubscribe links")
    
    if not emails:
        print("No emails with unsubscribe links found.")
        return
    
    unsubscribe_data = []
    
    for email_data in emails:
        if '|' in email_data:
            parts = email_data.split('|', 2)
            if len(parts) >= 3:
                sender, subject, content = parts
                links = extract_unsubscribe_links(content)
                
                if links:
                    unsubscribe_data.append({
                        'sender': sender.strip(),
                        'subject': subject.strip(),
                        'links': links
                    })
    
    print(f"\n📋 Found {len(unsubscribe_data)} emails with valid unsubscribe links:")
    
    for i, data in enumerate(unsubscribe_data, 1):
        print(f"\n{i}. From: {data['sender']}")
        print(f"   Subject: {data['subject']}")
        print(f"   Unsubscribe links:")
        for link in data['links']:
            if is_safe_unsubscribe_url(link):
                print(f"     • {link}")
            else:
                print(f"     • {link} (unsafe - skipped)")
    
    # Ask user what to do
    print(f"\n🤔 What would you like to do?")
    print("1. Open unsubscribe links in browser (manual)")
    print("2. Save report to file")
    print("3. Delete these emails")
    print("4. Do nothing")
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        open_unsubscribe_links(unsubscribe_data)
    elif choice == "2":
        save_report(unsubscribe_data)
    elif choice == "3":
        delete_unsubscribe_emails(unsubscribe_data)
    else:
        print("No action taken.")

def open_unsubscribe_links(unsubscribe_data):
    """Open unsubscribe links in browser"""
    print("\n🌐 Opening unsubscribe links in browser...")
    
    for data in unsubscribe_data:
        print(f"\nOpening links for: {data['sender']}")
        for link in data['links']:
            if is_safe_unsubscribe_url(link):
                try:
                    webbrowser.open(link)
                    print(f"  Opened: {link}")
                    time.sleep(2)  # Wait between opens
                except Exception as e:
                    print(f"  Error opening {link}: {e}")

def save_report(unsubscribe_data):
    """Save unsubscribe report to file"""
    report_path = os.path.expanduser("~/Desktop/unsubscribe_report.txt")
    
    with open(report_path, 'w') as f:
        f.write("Email Unsubscribe Report\n")
        f.write("=" * 50 + "\n\n")
        
        for i, data in enumerate(unsubscribe_data, 1):
            f.write(f"{i}. From: {data['sender']}\n")
            f.write(f"   Subject: {data['subject']}\n")
            f.write(f"   Unsubscribe links:\n")
            for link in data['links']:
                f.write(f"     • {link}\n")
            f.write("\n")
    
    print(f"📄 Report saved to: {report_path}")

def delete_unsubscribe_emails(unsubscribe_data):
    """Delete emails with unsubscribe links"""
    print("\n🗑️  Deleting emails with unsubscribe links...")
    
    # This would require more complex AppleScript to match and delete specific emails
    # For now, we'll use a simpler approach
    script = '''
    tell application "Mail"
        set inboxMessages to messages of inbox
        set deletedCount to 0
        
        repeat with msg in inboxMessages
            try
                set msgContent to content of msg
                if msgContent contains "unsubscribe" then
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
    
    result = osascript.run(script)
    deleted_count = result.out.strip() if result.out else "0"
    print(f"Deleted {deleted_count} emails with unsubscribe links")

if __name__ == "__main__":
    process_unsubscribe_links()
