#!/usr/bin/env python3
"""
Unsubscribe link detection and processing for Mail Organizer
"""

import re
import webbrowser
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.applescript_runner import AppleScriptRunner
from utils.logger import get_logger
from utils.file_utils import save_report
from config.keywords import UNSUBSCRIBE_PATTERNS

logger = get_logger(__name__)

class UnsubscribeDetector:
    """Handles unsubscribe link detection and processing"""
    
    def __init__(self):
        self.applescript_runner = AppleScriptRunner()
    
    def detect_unsubscribe_links(self) -> List[Dict[str, Any]]:
        """
        Detect all emails with unsubscribe links and extract the links
        
        Returns:
            List of dictionaries containing email info and unsubscribe links
        """
        logger.info("Detecting emails with unsubscribe links...")
        
        # Get emails with unsubscribe content
        script = '''
        tell application "Mail"
            set inboxMessages to messages of inbox
            set unsubscribeEmails to {}
            
            repeat with msg in inboxMessages
                try
                    set msgContent to content of msg
                    set msgSender to sender of msg
                    set msgSubject to subject of msg
                    set msgDate to date received of msg
                    
                    if msgContent contains "unsubscribe" then
                        set end of unsubscribeEmails to msgSender & "|" & msgSubject & "|" & msgDate & "|" & msgContent
                    end if
                on error
                    continue
                end try
            end repeat
            
            return unsubscribeEmails
        end tell
        '''
        
        result = self.applescript_runner.run_script(script, timeout=120)
        
        if not result['success']:
            logger.error(f"Failed to detect unsubscribe emails: {result['error']}")
            return []
        
        emails = []
        if result['output']:
            for email_data in result['output'].split(','):
                if '|' in email_data:
                    parts = email_data.split('|', 3)
                    if len(parts) >= 4:
                        sender, subject, date, content = parts
                        
                        # Extract unsubscribe links
                        links = self.extract_unsubscribe_links(content)
                        
                        if links:
                            emails.append({
                                'sender': sender.strip(),
                                'subject': subject.strip(),
                                'date': date.strip(),
                                'content': content.strip(),
                                'unsubscribe_links': links
                            })
        
        logger.info(f"Found {len(emails)} emails with unsubscribe links")
        return emails
    
    def extract_unsubscribe_links(self, content: str) -> List[str]:
        """Extract unsubscribe links from email content"""
        links = []
        
        for pattern in UNSUBSCRIBE_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            links.extend(matches)
        
        # Remove duplicates and clean up
        unique_links = list(set(links))
        cleaned_links = []
        
        for link in unique_links:
            # Clean up the link
            link = link.strip()
            if link.startswith('"') and link.endswith('"'):
                link = link[1:-1]
            if link.startswith("'") and link.endswith("'"):
                link = link[1:-1]
            
            if link and self.is_safe_unsubscribe_url(link):
                cleaned_links.append(link)
        
        return cleaned_links
    
    def is_safe_unsubscribe_url(self, url: str) -> bool:
        """Check if unsubscribe URL is safe to process"""
        try:
            parsed = urlparse(url)
            # Only allow http/https and mailto
            return parsed.scheme in ['http', 'https', 'mailto']
        except Exception:
            return False
    
    def open_unsubscribe_links(self, emails: List[Dict[str, Any]], delay: int = 2) -> Dict[str, Any]:
        """
        Open unsubscribe links in browser
        
        Args:
            emails: List of emails with unsubscribe links
            delay: Delay between opening links (seconds)
            
        Returns:
            Dictionary with results
        """
        logger.info(f"Opening unsubscribe links for {len(emails)} emails...")
        
        opened_count = 0
        error_count = 0
        results = []
        
        for email in emails:
            email_result = {
                'sender': email['sender'],
                'subject': email['subject'],
                'links_opened': [],
                'links_failed': []
            }
            
            for link in email['unsubscribe_links']:
                try:
                    webbrowser.open(link)
                    email_result['links_opened'].append(link)
                    opened_count += 1
                    logger.info(f"Opened unsubscribe link for {email['sender']}: {link}")
                    time.sleep(delay)  # Wait between opens
                except Exception as e:
                    email_result['links_failed'].append({'link': link, 'error': str(e)})
                    error_count += 1
                    logger.error(f"Failed to open link {link}: {e}")
            
            results.append(email_result)
        
        result = {
            'success': True,
            'total_emails': len(emails),
            'links_opened': opened_count,
            'links_failed': error_count,
            'results': results
        }
        
        logger.info(f"Unsubscribe link opening completed: {opened_count} opened, {error_count} failed")
        return result
    
    def delete_unsubscribe_emails(self, emails: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Delete emails that contain unsubscribe links
        
        Args:
            emails: List of emails to delete
            
        Returns:
            Dictionary with deletion results
        """
        logger.info(f"Deleting {len(emails)} emails with unsubscribe links...")
        
        # Get initial count
        initial_count = self.applescript_runner.get_inbox_count()
        
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
        
        result = self.applescript_runner.run_script(script, timeout=300)
        
        if not result['success']:
            logger.error(f"Failed to delete unsubscribe emails: {result['error']}")
            return {'success': False, 'error': result['error']}
        
        deleted_count = int(result['output']) if result['output'].isdigit() else 0
        final_count = self.applescript_runner.get_inbox_count()
        
        result = {
            'success': True,
            'initial_count': initial_count,
            'final_count': final_count,
            'deleted_count': deleted_count,
            'emails_processed': len(emails)
        }
        
        logger.info(f"Unsubscribe email deletion completed: {deleted_count} emails deleted")
        return result
    
    def save_unsubscribe_report(self, emails: List[Dict[str, Any]], filename: str = None) -> str:
        """
        Save unsubscribe analysis to a report file
        
        Args:
            emails: List of emails with unsubscribe links
            filename: Custom filename (optional)
            
        Returns:
            Path to saved report file
        """
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"unsubscribe_report_{timestamp}.txt"
        
        # Prepare report data
        report_data = {
            'report_type': 'Unsubscribe Analysis',
            'timestamp': datetime.now().isoformat(),
            'total_emails': len(emails),
            'emails': []
        }
        
        for i, email in enumerate(emails, 1):
            email_data = {
                'number': i,
                'sender': email['sender'],
                'subject': email['subject'],
                'date': email['date'],
                'unsubscribe_links': email['unsubscribe_links']
            }
            report_data['emails'].append(email_data)
        
        report_path = save_report(report_data, filename)
        
        if report_path:
            logger.info(f"Unsubscribe report saved to: {report_path}")
            return str(report_path)
        else:
            logger.error("Failed to save unsubscribe report")
            return ""
    
    def process_unsubscribe_emails(self, action: str = 'analyze') -> Dict[str, Any]:
        """
        Main function to process unsubscribe emails
        
        Args:
            action: Action to perform ('analyze', 'open', 'delete', 'report')
            
        Returns:
            Dictionary with processing results
        """
        logger.info(f"Processing unsubscribe emails with action: {action}")
        
        # Detect emails with unsubscribe links
        emails = self.detect_unsubscribe_links()
        
        if not emails:
            logger.info("No emails with unsubscribe links found")
            return {
                'success': True,
                'action': action,
                'emails_found': 0,
                'message': 'No emails with unsubscribe links found'
            }
        
        result = {
            'success': True,
            'action': action,
            'emails_found': len(emails),
            'emails': emails
        }
        
        if action == 'analyze':
            result['message'] = f'Found {len(emails)} emails with unsubscribe links'
            
        elif action == 'open':
            open_result = self.open_unsubscribe_links(emails)
            result.update(open_result)
            
        elif action == 'delete':
            delete_result = self.delete_unsubscribe_emails(emails)
            result.update(delete_result)
            
        elif action == 'report':
            report_path = self.save_unsubscribe_report(emails)
            result['report_path'] = report_path
            result['message'] = f'Report saved to {report_path}'
        
        return result
