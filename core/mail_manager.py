#!/usr/bin/env python3
"""
Core mail management functionality for Mail Organizer
"""

import re
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.applescript_runner import AppleScriptRunner
from utils.logger import get_logger
from config.keywords import (
    PROMOTIONAL_SUBJECT_KEYWORDS,
    PROMOTIONAL_SENDER_KEYWORDS,
    UNSUBSCRIBE_PATTERNS,
    PROMOTIONAL_CONTENT_PATTERNS
)

logger = get_logger(__name__)

class MailManager:
    """Core mail management operations"""
    
    def __init__(self):
        self.applescript_runner = AppleScriptRunner()
    
    def get_inbox_count(self) -> int:
        """Get current inbox email count"""
        return self.applescript_runner.get_inbox_count()
    
    def ensure_mail_running(self) -> bool:
        """Ensure Apple Mail is running"""
        return self.applescript_runner.ensure_mail_running()
    
    def mark_all_read(self) -> bool:
        """Mark all inbox emails as read"""
        logger.info("Marking all inbox emails as read")
        return self.applescript_runner.mark_all_read()
    
    def get_emails_with_unsubscribe(self) -> List[Dict[str, Any]]:
        """Get emails that contain unsubscribe links"""
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
            logger.error(f"Failed to get unsubscribe emails: {result['error']}")
            return []
        
        emails = []
        if result['output']:
            for email_data in result['output'].split(','):
                if '|' in email_data:
                    parts = email_data.split('|', 3)
                    if len(parts) >= 4:
                        emails.append({
                            'sender': parts[0].strip(),
                            'subject': parts[1].strip(),
                            'date': parts[2].strip(),
                            'content': parts[3].strip()
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
    
    def is_promotional_email(self, subject: str, sender: str, content: str = "") -> bool:
        """Check if an email is promotional based on subject, sender, and content"""
        subject_lower = subject.lower()
        sender_lower = sender.lower()
        content_lower = content.lower()
        
        # Check subject keywords
        for keyword in PROMOTIONAL_SUBJECT_KEYWORDS:
            if keyword.lower() in subject_lower:
                return True
        
        # Check sender keywords
        for keyword in PROMOTIONAL_SENDER_KEYWORDS:
            if keyword.lower() in sender_lower:
                return True
        
        # Check content patterns
        for pattern in PROMOTIONAL_CONTENT_PATTERNS:
            if pattern.lower() in content_lower:
                return True
        
        return False
    
    def analyze_inbox(self) -> Dict[str, Any]:
        """Analyze inbox and return statistics"""
        logger.info("Analyzing inbox...")
        
        script = '''
        tell application "Mail"
            set inboxMessages to messages of inbox
            set totalCount to count of inboxMessages
            set unreadCount to 0
            set promotionalCount to 0
            set unsubscribeCount to 0
            set senderCounts to {}
            
            repeat with msg in inboxMessages
                try
                    -- Count unread
                    if read status of msg is false then
                        set unreadCount to unreadCount + 1
                    end if
                    
                    -- Check for promotional content
                    set msgSubject to subject of msg
                    set msgSender to sender of msg
                    set msgContent to content of msg
                    
                    if msgSubject contains "unsubscribe" or msgSubject contains "promotional" or msgSubject contains "marketing" or msgSubject contains "newsletter" or msgSubject contains "offers" or msgSubject contains "sale" or msgSubject contains "discount" or msgSubject contains "deal" then
                        set promotionalCount to promotionalCount + 1
                    end if
                    
                    -- Check for unsubscribe links
                    if msgContent contains "unsubscribe" then
                        set unsubscribeCount to unsubscribeCount + 1
                    end if
                    
                    -- Count senders
                    set senderName to msgSender
                    if senderCounts contains senderName then
                        set senderCounts to senderCounts & {senderName}
                    end if
                    
                on error
                    continue
                end try
            end repeat
            
            return totalCount & "|" & unreadCount & "|" & promotionalCount & "|" & unsubscribeCount
        end tell
        '''
        
        result = self.applescript_runner.run_script(script, timeout=120)
        
        if not result['success']:
            logger.error(f"Failed to analyze inbox: {result['error']}")
            return {}
        
        if result['output'] and '|' in result['output']:
            parts = result['output'].split('|')
            if len(parts) >= 4:
                return {
                    'total_emails': int(parts[0]) if parts[0].isdigit() else 0,
                    'unread_emails': int(parts[1]) if parts[1].isdigit() else 0,
                    'promotional_emails': int(parts[2]) if parts[2].isdigit() else 0,
                    'unsubscribe_emails': int(parts[3]) if parts[3].isdigit() else 0
                }
        
        return {}
