#!/usr/bin/env python3
"""
Email cleanup engine for Mail Organizer
"""

from typing import Dict, Any, List
from datetime import datetime

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.applescript_runner import AppleScriptRunner
from utils.logger import get_logger
from utils.file_utils import save_report
from config.keywords import CLEANUP_LEVELS, AGE_THRESHOLDS
from core.mail_manager import MailManager

logger = get_logger(__name__)

class CleanupEngine:
    """Handles email cleanup operations"""
    
    def __init__(self):
        self.applescript_runner = AppleScriptRunner()
        self.mail_manager = MailManager()
    
    def cleanup_by_level(self, level: str, preserve_unsubscribe: bool = True) -> Dict[str, Any]:
        """
        Perform cleanup based on predefined levels
        
        Args:
            level: Cleanup level (gentle, moderate, aggressive, nuclear)
            preserve_unsubscribe: Whether to preserve emails with unsubscribe links
            
        Returns:
            Dictionary with cleanup results
        """
        if level not in CLEANUP_LEVELS:
            logger.error(f"Invalid cleanup level: {level}")
            return {'success': False, 'error': f'Invalid cleanup level: {level}'}
        
        config = CLEANUP_LEVELS[level]
        logger.info(f"Starting {level} cleanup...")
        
        # Get initial count
        initial_count = self.mail_manager.get_inbox_count()
        
        # Build criteria for cleanup
        criteria_parts = []
        
        # Add keyword criteria
        for keyword in config['keywords']:
            criteria_parts.append(f'msgSubject contains "{keyword}"')
        
        # Add sender criteria
        sender_keywords = ['noreply', 'no-reply', 'marketing', 'promo', 'offers', 'deals', 'newsletter']
        for keyword in sender_keywords:
            criteria_parts.append(f'msgSender contains "{keyword}"')
        
        # Combine criteria with OR
        criteria = ' or '.join(criteria_parts)
        
        # Perform cleanup
        deleted_count = self.applescript_runner.delete_emails_by_criteria(
            criteria, 
            preserve_unsubscribe=preserve_unsubscribe
        )
        
        # Get final count
        final_count = self.mail_manager.get_inbox_count()
        
        result = {
            'success': True,
            'level': level,
            'initial_count': initial_count,
            'final_count': final_count,
            'deleted_count': deleted_count,
            'preserve_unsubscribe': preserve_unsubscribe,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Cleanup completed: {deleted_count} emails deleted")
        return result
    
    def cleanup_by_keywords(self, keywords: List[str], preserve_unsubscribe: bool = True) -> Dict[str, Any]:
        """
        Perform cleanup based on custom keywords
        
        Args:
            keywords: List of keywords to match
            preserve_unsubscribe: Whether to preserve emails with unsubscribe links
            
        Returns:
            Dictionary with cleanup results
        """
        logger.info(f"Starting custom keyword cleanup with {len(keywords)} keywords...")
        
        # Get initial count
        initial_count = self.mail_manager.get_inbox_count()
        
        # Build criteria
        criteria_parts = []
        for keyword in keywords:
            criteria_parts.append(f'msgSubject contains "{keyword}"')
        
        criteria = ' or '.join(criteria_parts)
        
        # Perform cleanup
        deleted_count = self.applescript_runner.delete_emails_by_criteria(
            criteria,
            preserve_unsubscribe=preserve_unsubscribe
        )
        
        # Get final count
        final_count = self.mail_manager.get_inbox_count()
        
        result = {
            'success': True,
            'keywords': keywords,
            'initial_count': initial_count,
            'final_count': final_count,
            'deleted_count': deleted_count,
            'preserve_unsubscribe': preserve_unsubscribe,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Custom cleanup completed: {deleted_count} emails deleted")
        return result
    
    def cleanup_by_age(self, days: int) -> Dict[str, Any]:
        """
        Clean up emails older than specified days
        
        Args:
            days: Number of days (emails older than this will be deleted)
            
        Returns:
            Dictionary with cleanup results
        """
        logger.info(f"Starting age-based cleanup (older than {days} days)...")
        
        # Get initial count
        initial_count = self.mail_manager.get_inbox_count()
        
        script = f'''
        tell application "Mail"
            set inboxMessages to messages of inbox
            set deletedCount to 0
            set currentDate to current date
            
            repeat with msg in inboxMessages
                try
                    set msgDate to date received of msg
                    set daysOld to (currentDate - msgDate) / days
                    
                    if daysOld > {days} then
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
        
        result = self.applescript_runner.run_script(script, timeout=300)
        
        if not result['success']:
            logger.error(f"Age-based cleanup failed: {result['error']}")
            return {'success': False, 'error': result['error']}
        
        deleted_count = int(result['output']) if result['output'].isdigit() else 0
        final_count = self.mail_manager.get_inbox_count()
        
        result = {
            'success': True,
            'days_threshold': days,
            'initial_count': initial_count,
            'final_count': final_count,
            'deleted_count': deleted_count,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Age-based cleanup completed: {deleted_count} emails deleted")
        return result
    
    def cleanup_attachments(self) -> Dict[str, Any]:
        """
        Clean up emails with attachments (often promotional)
        
        Returns:
            Dictionary with cleanup results
        """
        logger.info("Starting attachment-based cleanup...")
        
        # Get initial count
        initial_count = self.mail_manager.get_inbox_count()
        
        script = '''
        tell application "Mail"
            set inboxMessages to messages of inbox
            set deletedCount to 0
            
            repeat with msg in inboxMessages
                try
                    if (count of mail attachments of msg) > 0 then
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
        
        result = self.applescript_runner.run_script(script, timeout=300)
        
        if not result['success']:
            logger.error(f"Attachment cleanup failed: {result['error']}")
            return {'success': False, 'error': result['error']}
        
        deleted_count = int(result['output']) if result['output'].isdigit() else 0
        final_count = self.mail_manager.get_inbox_count()
        
        result = {
            'success': True,
            'cleanup_type': 'attachments',
            'initial_count': initial_count,
            'final_count': final_count,
            'deleted_count': deleted_count,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Attachment cleanup completed: {deleted_count} emails deleted")
        return result
    
    def save_cleanup_report(self, cleanup_result: Dict[str, Any], filename: str = None) -> str:
        """
        Save cleanup results to a report file
        
        Args:
            cleanup_result: Results from cleanup operation
            filename: Custom filename (optional)
            
        Returns:
            Path to saved report file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cleanup_report_{timestamp}.txt"
        
        report_path = save_report(cleanup_result, filename)
        
        if report_path:
            logger.info(f"Cleanup report saved to: {report_path}")
            return str(report_path)
        else:
            logger.error("Failed to save cleanup report")
            return ""
