#!/usr/bin/env python3
"""
AppleScript execution utilities for Mail Organizer
"""

import subprocess
import time
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class AppleScriptRunner:
    """Handles AppleScript execution for Mail operations"""
    
    @staticmethod
    def run_script(script: str, timeout: int = 60) -> Dict[str, Any]:
        """
        Execute an AppleScript and return results
        
        Args:
            script: The AppleScript code to execute
            timeout: Maximum execution time in seconds
            
        Returns:
            Dict with 'success', 'output', 'error', and 'returncode'
        """
        try:
            logger.debug(f"Executing AppleScript: {script[:100]}...")
            
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout.strip(),
                'error': result.stderr.strip(),
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"AppleScript execution timed out after {timeout} seconds")
            return {
                'success': False,
                'output': '',
                'error': f'Script execution timed out after {timeout} seconds',
                'returncode': -1
            }
        except Exception as e:
            logger.error(f"Error executing AppleScript: {e}")
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'returncode': -1
            }
    
    @staticmethod
    def ensure_mail_running() -> bool:
        """Ensure Apple Mail is running"""
        try:
            # Check if Mail is running
            result = subprocess.run(
                ['pgrep', '-x', 'Mail'],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.info("Apple Mail is not running. Starting Mail...")
                subprocess.run(['open', '-a', 'Mail'])
                time.sleep(3)  # Wait for Mail to start
                return True
            return True
            
        except Exception as e:
            logger.error(f"Error checking/starting Mail: {e}")
            return False
    
    @staticmethod
    def get_inbox_count() -> int:
        """Get the current number of emails in inbox"""
        script = 'tell application "Mail" to return count of messages of inbox'
        result = AppleScriptRunner.run_script(script, timeout=10)
        
        if result['success'] and result['output'].isdigit():
            return int(result['output'])
        return 0
    
    @staticmethod
    def mark_all_read() -> bool:
        """Mark all inbox emails as read"""
        script = 'tell application "Mail" to set read status of every message of inbox to true'
        result = AppleScriptRunner.run_script(script, timeout=60)
        return result['success']
    
    @staticmethod
    def delete_emails_by_criteria(criteria: str, preserve_unsubscribe: bool = False) -> int:
        """
        Delete emails based on criteria
        
        Args:
            criteria: AppleScript criteria for email selection
            preserve_unsubscribe: Whether to preserve emails with unsubscribe links
            
        Returns:
            Number of emails deleted
        """
        if preserve_unsubscribe:
            script = f'''
            tell application "Mail"
                set inboxMessages to messages of inbox
                set deletedCount to 0
                set unsubscribeCount to 0
                
                repeat with msg in inboxMessages
                    try
                        set msgSubject to subject of msg
                        set msgSender to sender of msg
                        set msgContent to content of msg
                        set isPromo to false
                        set hasUnsubscribe to false
                        
                        -- Check criteria
                        if {criteria} then
                            set isPromo to true
                        end if
                        
                        -- Check for unsubscribe links
                        if msgContent contains "unsubscribe" then
                            set hasUnsubscribe to true
                        end if
                        
                        if isPromo and not hasUnsubscribe then
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
        else:
            script = f'''
            tell application "Mail"
                set inboxMessages to messages of inbox
                set deletedCount to 0
                
                repeat with msg in inboxMessages
                    try
                        if {criteria} then
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
        
        result = AppleScriptRunner.run_script(script, timeout=300)
        
        if result['success'] and result['output'].isdigit():
            return int(result['output'])
        return 0
