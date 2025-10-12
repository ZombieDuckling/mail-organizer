#!/usr/bin/env python3
"""
Inbox analysis script for Mail Organizer
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.mail_manager import MailManager
from core.unsubscribe_detector import UnsubscribeDetector
from utils.logger import setup_logger
from utils.file_utils import save_report

def main():
    """Main function for inbox analysis"""
    logger = setup_logger('inbox_analyzer')
    
    print("🔍 Inbox Analysis")
    print("=================")
    print()
    
    # Initialize components
    mail_manager = MailManager()
    unsubscribe_detector = UnsubscribeDetector()
    
    # Ensure Mail is running
    print("🔍 Checking if Apple Mail is running...")
    if not mail_manager.ensure_mail_running():
        print("❌ Failed to start Apple Mail")
        return 1
    
    # Get basic inbox statistics
    print("📊 Analyzing inbox...")
    analysis = mail_manager.analyze_inbox()
    
    if not analysis:
        print("❌ Failed to analyze inbox")
        return 1
    
    # Display results
    print("📈 Inbox Analysis Results:")
    print("==========================")
    print(f"📧 Total emails: {analysis['total_emails']:,}")
    print(f"📬 Unread emails: {analysis['unread_emails']:,}")
    print(f"📢 Promotional emails: {analysis['promotional_emails']:,}")
    print(f"🔗 Emails with unsubscribe links: {analysis['unsubscribe_emails']:,}")
    print()
    
    # Calculate percentages
    if analysis['total_emails'] > 0:
        unread_pct = (analysis['unread_emails'] / analysis['total_emails']) * 100
        promo_pct = (analysis['promotional_emails'] / analysis['total_emails']) * 100
        unsubscribe_pct = (analysis['unsubscribe_emails'] / analysis['total_emails']) * 100
        
        print("📊 Percentages:")
        print(f"   Unread: {unread_pct:.1f}%")
        print(f"   Promotional: {promo_pct:.1f}%")
        print(f"   With unsubscribe links: {unsubscribe_pct:.1f}%")
        print()
    
    # Analyze unsubscribe emails in detail
    if analysis['unsubscribe_emails'] > 0:
        print("🔍 Detailed Unsubscribe Analysis:")
        print("=================================")
        
        unsubscribe_emails = unsubscribe_detector.detect_unsubscribe_links()
        
        if unsubscribe_emails:
            print(f"📧 Found {len(unsubscribe_emails)} emails with unsubscribe links:")
            print()
            
            # Group by sender
            sender_counts = {}
            for email in unsubscribe_emails:
                sender = email['sender']
                if sender in sender_counts:
                    sender_counts[sender] += 1
                else:
                    sender_counts[sender] = 1
            
            # Sort by count
            sorted_senders = sorted(sender_counts.items(), key=lambda x: x[1], reverse=True)
            
            print("📊 Top senders with unsubscribe links:")
            for i, (sender, count) in enumerate(sorted_senders[:10], 1):
                print(f"   {i:2d}. {sender} ({count} email{'s' if count > 1 else ''})")
            
            if len(sorted_senders) > 10:
                print(f"   ... and {len(sorted_senders) - 10} more senders")
            print()
    
    # Recommendations
    print("💡 Recommendations:")
    print("==================")
    
    if analysis['promotional_emails'] > analysis['total_emails'] * 0.3:
        print("   🧹 Consider running a cleanup to remove promotional emails")
    
    if analysis['unread_emails'] > analysis['total_emails'] * 0.5:
        print("   📧 Consider marking all emails as read to clear notifications")
    
    if analysis['unsubscribe_emails'] > 0:
        print("   🔗 Review unsubscribe emails to manually unsubscribe from unwanted senders")
    
    if analysis['total_emails'] > 1000:
        print("   📦 Your inbox is quite large - consider regular cleanup")
    
    print()
    
    # Save detailed report
    report_data = {
        'analysis_type': 'Inbox Analysis',
        'timestamp': analysis.get('timestamp', ''),
        'statistics': analysis,
        'unsubscribe_details': {
            'total_emails_with_unsubscribe': len(unsubscribe_emails) if 'unsubscribe_emails' in locals() else 0,
            'top_senders': sorted_senders[:20] if 'sorted_senders' in locals() else []
        },
        'recommendations': [
            'Consider running a cleanup to remove promotional emails' if analysis['promotional_emails'] > analysis['total_emails'] * 0.3 else None,
            'Consider marking all emails as read to clear notifications' if analysis['unread_emails'] > analysis['total_emails'] * 0.5 else None,
            'Review unsubscribe emails to manually unsubscribe from unwanted senders' if analysis['unsubscribe_emails'] > 0 else None,
            'Your inbox is quite large - consider regular cleanup' if analysis['total_emails'] > 1000 else None
        ]
    }
    
    # Remove None recommendations
    report_data['recommendations'] = [r for r in report_data['recommendations'] if r is not None]
    
    report_path = save_report(report_data, "inbox_analysis_report.txt")
    if report_path:
        print(f"📄 Detailed report saved to: {report_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
