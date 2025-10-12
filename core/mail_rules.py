#!/usr/bin/env python3
"""
Mail rules management for Mail Organizer
"""

from typing import Dict, Any, List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.applescript_runner import AppleScriptRunner
from utils.logger import get_logger
from config.keywords import PROMOTIONAL_SUBJECT_KEYWORDS, PROMOTIONAL_SENDER_KEYWORDS

logger = get_logger(__name__)

class MailRulesManager:
    """Handles creation and management of Mail rules"""
    
    def __init__(self):
        self.applescript_runner = AppleScriptRunner()
    
    def create_promotional_rule(self, rule_name: str = "Auto-Delete Promotional Emails") -> Dict[str, Any]:
        """
        Create a mail rule to automatically delete promotional emails
        
        Args:
            rule_name: Name for the mail rule
            
        Returns:
            Dictionary with creation results
        """
        logger.info(f"Creating promotional mail rule: {rule_name}")
        
        # Build conditions for the rule
        conditions = []
        
        # Add subject conditions
        for keyword in PROMOTIONAL_SUBJECT_KEYWORDS[:10]:  # Limit to first 10 to avoid rule complexity
            conditions.append(f'set condition to make new rule condition with properties {{rule type:subject contains value, expression:"{keyword}"}}')
        
        # Add sender conditions
        for keyword in PROMOTIONAL_SENDER_KEYWORDS[:5]:  # Limit to first 5
            conditions.append(f'set condition to make new rule condition with properties {{rule type:sender contains value, expression:"{keyword}"}}')
        
        conditions_script = '\n'.join(conditions)
        
        script = f'''
        tell application "Mail"
            activate
            
            try
                -- Create a rule for promotional emails
                set newRule to make new rule with properties {{name:"{rule_name}", enabled:true}}
                
                -- Add conditions for the rule
                {conditions_script}
                
                -- Add action to move to trash
                set action1 to make new rule action with properties {{rule type:move message, destination:trash mailbox}}
                
                return "success"
            on error errorMessage
                return "error:" & errorMessage
            end try
        end tell
        '''
        
        result = self.applescript_runner.run_script(script, timeout=60)
        
        if result['success'] and 'success' in result['output']:
            logger.info(f"Successfully created promotional mail rule: {rule_name}")
            return {
                'success': True,
                'rule_name': rule_name,
                'message': f'Mail rule "{rule_name}" created successfully'
            }
        else:
            error_msg = result['output'] if result['output'] else result['error']
            logger.error(f"Failed to create promotional mail rule: {error_msg}")
            return {
                'success': False,
                'rule_name': rule_name,
                'error': error_msg
            }
    
    def create_unsubscribe_rule(self, rule_name: str = "Preserve Unsubscribe Emails") -> Dict[str, Any]:
        """
        Create a mail rule to preserve emails with unsubscribe links
        
        Args:
            rule_name: Name for the mail rule
            
        Returns:
            Dictionary with creation results
        """
        logger.info(f"Creating unsubscribe preservation rule: {rule_name}")
        
        script = f'''
        tell application "Mail"
            activate
            
            try
                -- Create a rule to preserve unsubscribe emails
                set newRule to make new rule with properties {{name:"{rule_name}", enabled:true}}
                
                -- Add condition for unsubscribe content
                set condition to make new rule condition with properties {{rule type:message content contains value, expression:"unsubscribe"}}
                
                -- Add action to move to a special folder (or do nothing to preserve in inbox)
                -- For now, we'll just mark them as important
                set action1 to make new rule action with properties {{rule type:set color of message, color:red}}
                
                return "success"
            on error errorMessage
                return "error:" & errorMessage
            end try
        end tell
        '''
        
        result = self.applescript_runner.run_script(script, timeout=60)
        
        if result['success'] and 'success' in result['output']:
            logger.info(f"Successfully created unsubscribe preservation rule: {rule_name}")
            return {
                'success': True,
                'rule_name': rule_name,
                'message': f'Mail rule "{rule_name}" created successfully'
            }
        else:
            error_msg = result['output'] if result['output'] else result['error']
            logger.error(f"Failed to create unsubscribe preservation rule: {error_msg}")
            return {
                'success': False,
                'rule_name': rule_name,
                'error': error_msg
            }
    
    def create_sender_specific_rule(self, sender_pattern: str, action: str = "delete", rule_name: str = None) -> Dict[str, Any]:
        """
        Create a mail rule for a specific sender pattern
        
        Args:
            sender_pattern: Pattern to match in sender field
            action: Action to take ('delete', 'move_to_trash', 'mark_read')
            rule_name: Name for the rule (auto-generated if not provided)
            
        Returns:
            Dictionary with creation results
        """
        if rule_name is None:
            rule_name = f"Rule for {sender_pattern}"
        
        logger.info(f"Creating sender-specific rule: {rule_name}")
        
        # Determine action
        if action == "delete" or action == "move_to_trash":
            action_script = 'set action1 to make new rule action with properties {rule type:move message, destination:trash mailbox}'
        elif action == "mark_read":
            action_script = 'set action1 to make new rule action with properties {rule type:mark message as read}'
        else:
            return {
                'success': False,
                'error': f'Invalid action: {action}'
            }
        
        script = f'''
        tell application "Mail"
            activate
            
            try
                -- Create a rule for specific sender
                set newRule to make new rule with properties {{name:"{rule_name}", enabled:true}}
                
                -- Add condition for sender
                set condition to make new rule condition with properties {{rule type:sender contains value, expression:"{sender_pattern}"}}
                
                -- Add action
                {action_script}
                
                return "success"
            on error errorMessage
                return "error:" & errorMessage
            end try
        end tell
        '''
        
        result = self.applescript_runner.run_script(script, timeout=60)
        
        if result['success'] and 'success' in result['output']:
            logger.info(f"Successfully created sender-specific rule: {rule_name}")
            return {
                'success': True,
                'rule_name': rule_name,
                'sender_pattern': sender_pattern,
                'action': action,
                'message': f'Mail rule "{rule_name}" created successfully'
            }
        else:
            error_msg = result['output'] if result['output'] else result['error']
            logger.error(f"Failed to create sender-specific rule: {error_msg}")
            return {
                'success': False,
                'rule_name': rule_name,
                'error': error_msg
            }
    
    def list_existing_rules(self) -> Dict[str, Any]:
        """
        List existing mail rules
        
        Returns:
            Dictionary with list of existing rules
        """
        logger.info("Listing existing mail rules...")
        
        script = '''
        tell application "Mail"
            set ruleList to {}
            set ruleNames to name of every rule
            
            repeat with ruleName in ruleNames
                set end of ruleList to ruleName
            end repeat
            
            return ruleList
        end tell
        '''
        
        result = self.applescript_runner.run_script(script, timeout=30)
        
        if result['success']:
            rules = result['output'].split(',') if result['output'] else []
            cleaned_rules = [rule.strip() for rule in rules if rule.strip()]
            
            logger.info(f"Found {len(cleaned_rules)} existing mail rules")
            return {
                'success': True,
                'rules': cleaned_rules,
                'count': len(cleaned_rules)
            }
        else:
            logger.error(f"Failed to list mail rules: {result['error']}")
            return {
                'success': False,
                'error': result['error']
            }
    
    def create_comprehensive_rules(self) -> Dict[str, Any]:
        """
        Create a comprehensive set of mail rules for email organization
        
        Returns:
            Dictionary with creation results
        """
        logger.info("Creating comprehensive mail rules...")
        
        results = []
        
        # Create promotional email rule
        promo_result = self.create_promotional_rule("Auto-Delete Promotional Emails")
        results.append(promo_result)
        
        # Create unsubscribe preservation rule
        unsubscribe_result = self.create_unsubscribe_rule("Preserve Unsubscribe Emails")
        results.append(unsubscribe_result)
        
        # Create social media notification rule
        social_result = self.create_sender_specific_rule(
            "notification", 
            "delete", 
            "Delete Social Media Notifications"
        )
        results.append(social_result)
        
        # Count successful creations
        successful = sum(1 for result in results if result['success'])
        total = len(results)
        
        return {
            'success': successful > 0,
            'total_rules_attempted': total,
            'successful_rules': successful,
            'failed_rules': total - successful,
            'results': results
        }
