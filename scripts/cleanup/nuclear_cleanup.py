#!/usr/bin/env python3
"""
Nuclear cleanup script for Mail Organizer
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.cleanup_engine import CleanupEngine
from utils.logger import setup_logger

def main():
    """Main function for nuclear cleanup"""
    logger = setup_logger('nuclear_cleanup')
    
    print("💥 Nuclear Email Cleanup")
    print("=======================")
    print()
    print("⚠️  WARNING: This is an aggressive cleanup that will delete many emails!")
    print("   - Promotional emails")
    print("   - Social media notifications")
    print("   - System notifications")
    print("   - Emails with attachments")
    print("   - Old emails (30+ days)")
    print()
    
    # Confirm with user
    try:
        confirm = input("Are you sure you want to proceed? (type 'YES' to confirm): ")
        if confirm != 'YES':
            print("❌ Nuclear cleanup cancelled.")
            return 0
    except KeyboardInterrupt:
        print("\n❌ Nuclear cleanup cancelled.")
        return 0
    
    # Initialize cleanup engine
    cleanup_engine = CleanupEngine()
    
    total_deleted = 0
    results = []
    
    # 1. Nuclear cleanup by keywords
    print("🧹 Step 1: Aggressive keyword cleanup...")
    result1 = cleanup_engine.cleanup_by_level('nuclear', preserve_unsubscribe=False)
    if result1['success']:
        total_deleted += result1['deleted_count']
        results.append(result1)
        print(f"   ✅ Deleted {result1['deleted_count']:,} emails by keywords")
    
    # 2. Age-based cleanup
    print("🧹 Step 2: Age-based cleanup (30+ days)...")
    result2 = cleanup_engine.cleanup_by_age(30)
    if result2['success']:
        total_deleted += result2['deleted_count']
        results.append(result2)
        print(f"   ✅ Deleted {result2['deleted_count']:,} old emails")
    
    # 3. Attachment cleanup
    print("🧹 Step 3: Attachment cleanup...")
    result3 = cleanup_engine.cleanup_attachments()
    if result3['success']:
        total_deleted += result3['deleted_count']
        results.append(result3)
        print(f"   ✅ Deleted {result3['deleted_count']:,} emails with attachments")
    
    # Get final count
    final_count = cleanup_engine.mail_manager.get_inbox_count()
    
    print()
    print("💥 NUCLEAR CLEANUP COMPLETE!")
    print("=============================")
    print(f"🗑️  Total emails deleted: {total_deleted:,}")
    print(f"📊 Final inbox count: {final_count:,}")
    
    if total_deleted > 0:
        # Calculate percentage based on initial count from first result
        if results and 'initial_count' in results[0]:
            initial_count = results[0]['initial_count']
            percentage = (total_deleted / initial_count) * 100
            print(f"💡 Your inbox is {percentage:.1f}% cleaner!")
    
    print()
    print("🔍 Remaining emails are likely:")
    print("   • Recent personal emails")
    print("   • Important business emails")
    print("   • Emails without promotional content")
    print()
    print("⚠️  WARNING: This was an aggressive cleanup!")
    print("   Check your Trash folder to review deleted emails!")
    
    # Save comprehensive report
    comprehensive_result = {
        'success': True,
        'cleanup_type': 'nuclear',
        'total_deleted': total_deleted,
        'final_count': final_count,
        'steps': results,
        'timestamp': results[0]['timestamp'] if results else None
    }
    
    report_path = cleanup_engine.save_cleanup_report(comprehensive_result, "nuclear_cleanup_report.txt")
    if report_path:
        print(f"📄 Comprehensive report saved to: {report_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
