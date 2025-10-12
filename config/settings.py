#!/usr/bin/env python3
"""
Configuration settings for Mail Organizer
"""

import os
import json
from pathlib import Path

class Settings:
    """Configuration management for Mail Organizer"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.settings_file = self.config_dir / 'settings.json'
        self.default_settings = {
            'auto_refresh': True,
            'refresh_interval': 30,
            'log_level': 'INFO',
            'backup_before_cleanup': True,
            'show_confirmation': True,
            'gui_theme': 'default',
            'window_size': {'width': 800, 'height': 600},
            'last_cleanup_date': None,
            'cleanup_stats': {
                'total_emails_deleted': 0,
                'total_cleanups': 0,
                'last_cleanup_count': 0
            }
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or return defaults"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    settings = self.default_settings.copy()
                    settings.update(loaded_settings)
                    return settings
            except (json.JSONDecodeError, IOError):
                return self.default_settings.copy()
        return self.default_settings.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except IOError:
            return False
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        return self.save_settings()
    
    def update_cleanup_stats(self, emails_deleted):
        """Update cleanup statistics"""
        stats = self.settings['cleanup_stats']
        stats['total_emails_deleted'] += emails_deleted
        stats['total_cleanups'] += 1
        stats['last_cleanup_count'] = emails_deleted
        self.settings['last_cleanup_date'] = str(Path().cwd())
        return self.save_settings()

# Global settings instance
settings = Settings()
