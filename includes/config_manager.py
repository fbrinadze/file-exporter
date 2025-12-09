"""
Configuration Manager
=====================
Manages application settings using JSON file instead of .env
"""

import json
import os


class ConfigManager:
    """Manages application configuration in a JSON file."""
    
    def __init__(self, config_file='config.json'):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.default_config = {
            'email': {
                'enabled': False,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'username': '',
                'password': '',
                'from_email': '',
                'to_email': ''
            },
            'teams': {
                'enabled': False,
                'webhook_url': ''
            }
        }
    
    def load(self):
        """
        Load configuration from file.
        
        Returns:
            dict: Configuration dictionary
        """
        if not os.path.exists(self.config_file):
            return self.default_config.copy()
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self._merge_with_defaults(config)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()
    
    def save(self, config):
        """
        Save configuration to file.
        
        Args:
            config: Configuration dictionary to save
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _merge_with_defaults(self, config):
        """
        Merge loaded config with defaults to ensure all keys exist.
        
        Args:
            config: Loaded configuration
            
        Returns:
            dict: Merged configuration
        """
        merged = self.default_config.copy()
        
        if 'email' in config:
            merged['email'].update(config['email'])
        if 'teams' in config:
            merged['teams'].update(config['teams'])
        
        return merged
    
    def get_email_config(self):
        """Get email configuration."""
        config = self.load()
        return config.get('email', self.default_config['email'])
    
    def get_teams_config(self):
        """Get Teams configuration."""
        config = self.load()
        return config.get('teams', self.default_config['teams'])
    
    def is_email_enabled(self):
        """Check if email notifications are enabled."""
        return self.get_email_config().get('enabled', False)
    
    def is_teams_enabled(self):
        """Check if Teams notifications are enabled."""
        return self.get_teams_config().get('enabled', False)
