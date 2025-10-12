#!/usr/bin/env python3
"""
Unsubscribe analysis script for Mail Organizer
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.unsubscribe_detector import UnsubscribeDetector
from utils.logger import setup_logger

def main():
    """Main function for unsubscribe analysis"""
    logger = setup_logger('unsubscribe_analyzer')
    
    print("🔗 Unsubscribe Link Analysis")
    print("============================")
    print()
    
    # Initialize unsubscribe detector
    unsubscribe_detector = UnsubscribeDetector()
    
    # Detect emails with unsubscribe links
    print("🔍 Scanning emails for unsubscribe links...")
    emails = unsubscribe_detector.detect_unsubscribe_links()
    
    if not emails:
        print("✅ No emails with unsubscribe links found!")
        print("   Your inbox is clean of unsubscribe emails.")
        return 0
    
    print(f"📧 Found {len(emails)} emails with unsubscribe links:")
    print()
    
    # Display results
    for i, email in enumerate(emails, 1):
        print(f"{i:2d}. From: {email['sender']}")
        print(f"    Subject: {email['subject']}")
        print(f"    Date: {email['date']}")
        print(f"    Unsubscribe links ({len(email['unsubscribe_links'])}):")
        
        for j, link in enumerate(email['unsubscribe_links'], 1):
            print(f"       {j}. {link}")
        print()
    
    # Group by sender
    sender_counts = {}
    for email in emails:
        sender = email['sender']
        if sender in sender_counts:
            sender_counts[sender] += 1
        else:
            sender_counts[sender] = 1
    
    # Sort by count
    sorted_senders = sorted(sender_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("📊 Summary by Sender:")
    print("====================")
    for i, (sender, count) in enumerate(sorted_senders, 1):
        print(f"{i:2d}. {sender} ({count} email{'s' if count > 1 else ''})")
    print()
    
    # Ask user what to do
    print("🤔 What would you like to do?")
    print("1. Open unsubscribe links in browser (manual)")
    print("2. Save detailed report to file")
    print("3. Delete these emails")
    print("4. Do nothing")
    print()
    
    try:
        choice = input("Enter your choice (1-4): ").strip()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled.")
        return 0
    
    if choice == "1":
        print("\n🌐 Opening unsubscribe links in browser...")
        result = unsubscribe_detector.open_unsubscribe_links(emails)
        
        if result['success']:
            print(f"✅ Opened {result['links_opened']} unsubscribe links")
            if result['links_failed'] > 0:
                print(f"⚠️  Failed to open {result['links_failed']} links")
        else:
            print("❌ Failed to open unsubscribe links")
    
    elif choice == "2":
        print("\n📄 Saving detailed report...")
        report_path = unsubscribe_detector.save_unsubscribe_report(emails)
        
        if report_path:
            print(f"✅ Report saved to: {report_path}")
        else:
            print("❌ Failed to save report")
    
    elif choice == "3":
        print("\n🗑️  Deleting emails with unsubscribe links...")
        result = unsubscribe_detector.delete_unsubscribe_emails(emails)
        
        if result['success']:
            print(f"✅ Deleted {result['deleted_count']} emails with unsubscribe links")
            print(f"📊 Remaining emails: {result['final_count']:,}")
        else:
            print(f"❌ Failed to delete emails: {result.get('error', 'Unknown error')}")
    
    else:
        print("No action taken.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
