#!/usr/bin/env python3
"""
Main entry point for Mail Organizer
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import setup_logger
from core.mail_manager import MailManager
from core.cleanup_engine import CleanupEngine
from core.unsubscribe_detector import UnsubscribeDetector
from core.mail_rules import MailRulesManager

def show_menu():
    """Display the main menu"""
    print("🍎 Mail Organizer Pro")
    print("====================")
    print()
    print("What would you like to do?")
    print()
    print("📧 Email Management:")
    print("  1. Quick Cleanup (gentle)")
    print("  2. Smart Cleanup (preserve unsubscribe)")
    print("  3. Nuclear Cleanup (aggressive)")
    print("  4. Mark All as Read")
    print()
    print("🔍 Analysis:")
    print("  5. Analyze Inbox")
    print("  6. Check Unsubscribe Links")
    print()
    print("⚙️  Tools:")
    print("  7. Create Mail Rules")
    print("  8. Launch GUI")
    print()
    print("  0. Exit")
    print()

def main():
    """Main function"""
    logger = setup_logger('main')
    
    # Initialize components
    mail_manager = MailManager()
    cleanup_engine = CleanupEngine()
    unsubscribe_detector = UnsubscribeDetector()
    mail_rules_manager = MailRulesManager()
    
    # Ensure Mail is running
    if not mail_manager.ensure_mail_running():
        print("❌ Failed to start Apple Mail. Please ensure Mail is installed and accessible.")
        return 1
    
    while True:
        try:
            show_menu()
            
            # Get current inbox count
            current_count = mail_manager.get_inbox_count()
            print(f"📊 Current inbox: {current_count:,} emails")
            print()
            
            choice = input("Enter your choice (0-8): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            
            elif choice == "1":
                print("🚀 Running Quick Cleanup...")
                result = cleanup_engine.cleanup_by_level('gentle', preserve_unsubscribe=True)
                if result['success']:
                    print(f"✅ Deleted {result['deleted_count']:,} emails")
                else:
                    print(f"❌ Cleanup failed: {result.get('error', 'Unknown error')}")
            
            elif choice == "2":
                print("🧠 Running Smart Cleanup...")
                result = cleanup_engine.cleanup_by_level('moderate', preserve_unsubscribe=True)
                if result['success']:
                    print(f"✅ Deleted {result['deleted_count']:,} emails")
                else:
                    print(f"❌ Cleanup failed: {result.get('error', 'Unknown error')}")
            
            elif choice == "3":
                print("💥 Running Nuclear Cleanup...")
                confirm = input("⚠️  This is aggressive! Continue? (y/N): ")
                if confirm.lower() in ['y', 'yes']:
                    result = cleanup_engine.cleanup_by_level('nuclear', preserve_unsubscribe=False)
                    if result['success']:
                        print(f"✅ Deleted {result['deleted_count']:,} emails")
                    else:
                        print(f"❌ Cleanup failed: {result.get('error', 'Unknown error')}")
                else:
                    print("❌ Nuclear cleanup cancelled.")
            
            elif choice == "4":
                print("📧 Marking all emails as read...")
                success = mail_manager.mark_all_read()
                if success:
                    print("✅ All emails marked as read!")
                else:
                    print("❌ Failed to mark emails as read")
            
            elif choice == "5":
                print("🔍 Analyzing inbox...")
                analysis = mail_manager.analyze_inbox()
                if analysis:
                    print(f"📊 Total: {analysis['total_emails']:,}")
                    print(f"📬 Unread: {analysis['unread_emails']:,}")
                    print(f"📢 Promotional: {analysis['promotional_emails']:,}")
                    print(f"🔗 With unsubscribe: {analysis['unsubscribe_emails']:,}")
                else:
                    print("❌ Failed to analyze inbox")
            
            elif choice == "6":
                print("🔗 Checking unsubscribe links...")
                result = unsubscribe_detector.process_unsubscribe_emails('analyze')
                if result['success']:
                    print(f"📧 Found {result['emails_found']} emails with unsubscribe links")
                else:
                    print("❌ Failed to check unsubscribe links")
            
            elif choice == "7":
                print("⚙️  Creating mail rules...")
                result = mail_rules_manager.create_comprehensive_rules()
                if result['success']:
                    print(f"✅ Created {result['successful_rules']} mail rules")
                else:
                    print("❌ Failed to create mail rules")
            
            elif choice == "8":
                print("🚀 Launching GUI...")
                try:
                    from gui.gui_launcher import main as gui_main
                    gui_main()
                except Exception as e:
                    print(f"❌ Failed to launch GUI: {e}")
            
            else:
                print("❌ Invalid choice. Please try again.")
            
            print()
            input("Press Enter to continue...")
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            logger.error(f"Error in main loop: {e}")
            print()
            input("Press Enter to continue...")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
