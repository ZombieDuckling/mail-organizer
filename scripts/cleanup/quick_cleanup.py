#!/usr/bin/env python3
"""
Quick cleanup script for Mail Organizer
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.cleanup_engine import CleanupEngine
from utils.logger import setup_logger

def main():
    """Main function for quick cleanup"""
    logger = setup_logger('quick_cleanup')
    
    print("🚀 Quick Email Cleanup")
    print("=====================")
    print()
    
    # Initialize cleanup engine
    cleanup_engine = CleanupEngine()
    
    # Perform gentle cleanup
    print("Starting quick cleanup (gentle mode)...")
    result = cleanup_engine.cleanup_by_level('gentle', preserve_unsubscribe=True)
    
    if result['success']:
        print(f"✅ Cleanup completed successfully!")
        print(f"📊 Initial emails: {result['initial_count']:,}")
        print(f"📊 Final emails: {result['final_count']:,}")
        print(f"🗑️  Emails deleted: {result['deleted_count']:,}")
        
        if result['deleted_count'] > 0:
            percentage = (result['deleted_count'] / result['initial_count']) * 100
            print(f"💡 Your inbox is {percentage:.1f}% cleaner!")
        
        # Save report
        report_path = cleanup_engine.save_cleanup_report(result)
        if report_path:
            print(f"📄 Report saved to: {report_path}")
    else:
        print(f"❌ Cleanup failed: {result.get('error', 'Unknown error')}")
        return 1
    
    print()
    print("💡 Tips:")
    print("   - Check your Trash folder to review deleted emails")
    print("   - You can restore any emails you want to keep")
    print("   - Run this script regularly to keep your inbox clean")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
