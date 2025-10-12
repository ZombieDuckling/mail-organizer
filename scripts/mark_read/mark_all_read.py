#!/usr/bin/env python3
"""
Mark all emails as read script for Mail Organizer
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.mail_manager import MailManager
from utils.logger import setup_logger

def main():
    """Main function for marking all emails as read"""
    logger = setup_logger('mark_all_read')
    
    print("📧 Mark All Emails as Read")
    print("==========================")
    print()
    
    # Initialize mail manager
    mail_manager = MailManager()
    
    # Ensure Mail is running
    print("🔍 Checking if Apple Mail is running...")
    if not mail_manager.ensure_mail_running():
        print("❌ Failed to start Apple Mail")
        return 1
    
    # Get current count
    current_count = mail_manager.get_inbox_count()
    print(f"📊 Current inbox: {current_count:,} emails")
    print()
    
    # Confirm with user
    try:
        confirm = input("Mark all inbox emails as read? (y/N): ")
        if confirm.lower() not in ['y', 'yes']:
            print("❌ Operation cancelled.")
            return 0
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled.")
        return 0
    
    # Mark all as read
    print("🚀 Marking all inbox emails as read...")
    success = mail_manager.mark_all_read()
    
    if success:
        print("✅ All inbox emails marked as read!")
        print()
        print("💡 Your inbox is now clean of unread email notifications!")
        print("   - All emails are now marked as read")
        print("   - No emails were deleted")
        print("   - You can still access all your emails")
    else:
        print("❌ Failed to mark emails as read")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
