#!/usr/bin/env python3
"""
Smart cleanup script for Mail Organizer
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.cleanup_engine import CleanupEngine
from core.unsubscribe_detector import UnsubscribeDetector
from utils.logger import setup_logger

def main():
    """Main function for smart cleanup"""
    logger = setup_logger('smart_cleanup')
    
    print("🧠 Smart Email Cleanup")
    print("=====================")
    print()
    
    # Initialize components
    cleanup_engine = CleanupEngine()
    unsubscribe_detector = UnsubscribeDetector()
    
    # First, analyze unsubscribe emails
    print("🔍 Analyzing emails with unsubscribe links...")
    unsubscribe_emails = unsubscribe_detector.detect_unsubscribe_links()
    
    if unsubscribe_emails:
        print(f"📧 Found {len(unsubscribe_emails)} emails with unsubscribe links:")
        for i, email in enumerate(unsubscribe_emails[:5], 1):  # Show first 5
            print(f"   {i}. From: {email['sender']}")
            print(f"      Subject: {email['subject']}")
            print(f"      Links: {len(email['unsubscribe_links'])} unsubscribe link(s)")
        
        if len(unsubscribe_emails) > 5:
            print(f"   ... and {len(unsubscribe_emails) - 5} more")
        print()
    
    # Perform moderate cleanup (preserving unsubscribe emails)
    print("🧹 Starting smart cleanup (preserving unsubscribe emails)...")
    result = cleanup_engine.cleanup_by_level('moderate', preserve_unsubscribe=True)
    
    if result['success']:
        print(f"✅ Smart cleanup completed successfully!")
        print(f"📊 Initial emails: {result['initial_count']:,}")
        print(f"📊 Final emails: {result['final_count']:,}")
        print(f"🗑️  Emails deleted: {result['deleted_count']:,}")
        print(f"📧 Emails with unsubscribe links preserved: {len(unsubscribe_emails)}")
        
        if result['deleted_count'] > 0:
            percentage = (result['deleted_count'] / result['initial_count']) * 100
            print(f"💡 Your inbox is {percentage:.1f}% cleaner!")
        
        # Save report
        report_path = cleanup_engine.save_cleanup_report(result)
        if report_path:
            print(f"📄 Cleanup report saved to: {report_path}")
        
        # Save unsubscribe report
        if unsubscribe_emails:
            unsubscribe_report = unsubscribe_detector.save_unsubscribe_report(unsubscribe_emails)
            if unsubscribe_report:
                print(f"📄 Unsubscribe report saved to: {unsubscribe_report}")
    else:
        print(f"❌ Smart cleanup failed: {result.get('error', 'Unknown error')}")
        return 1
    
    print()
    print("💡 Next steps:")
    print("   - Review the unsubscribe report to manually unsubscribe from unwanted senders")
    print("   - Check your Trash folder to review deleted emails")
    print("   - You can restore any emails you want to keep")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
