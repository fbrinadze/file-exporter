"""
MS Teams Notification Module
=============================
Sends notifications to MS Teams channel via webhook.

Requirements:
    - requests (pip install requests)
"""

import os
import requests
from .config_manager import ConfigManager


def load_teams_config():
    """
    Load MS Teams webhook URL from config file.
    
    Returns:
        str: Teams webhook URL
        
    Raises:
        ValueError: If webhook URL is missing
    """
    config_mgr = ConfigManager()
    teams_config = config_mgr.get_teams_config()
    
    webhook_url = teams_config.get('webhook_url')
    
    if not webhook_url:
        raise ValueError(
            "Missing Teams webhook URL. Please configure in Settings."
        )
    
    return webhook_url


def is_enabled():
    """
    Check if Teams notifications are enabled.
    
    Returns:
        bool: True if enabled, False otherwise
    """
    config_mgr = ConfigManager()
    return config_mgr.is_teams_enabled()


def send_teams_message(title, message, color="0078D4", webhook_url=None):
    """
    Send a message to MS Teams using webhook.
    
    Args:
        title: Message title
        message: The message text to send
        color: Hex color for the message card (default: blue)
        webhook_url: Optional webhook URL (if None, loads from config)
        
    Returns:
        bool: True if message sent successfully, False otherwise
    """
    try:
        if webhook_url is None:
            webhook_url = load_teams_config()
        
        # Create adaptive card payload
        payload = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "themeColor": color,
            "title": title,
            "text": message
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to send Teams message. Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Failed to send Teams message: {e}")
        return False


def send_success_notification(file_count, output_file):
    """
    Send a success notification to MS Teams.
    
    Args:
        file_count: Number of files exported
        output_file: Path to the output Excel file
    """
    if not is_enabled():
        return False
    
    title = "✅ File Export Complete!"
    message = f"Successfully exported **{file_count}** files to:\n\n`{os.path.basename(output_file)}`"
    return send_teams_message(title, message, color="28A745")  # Green


def send_failure_notification(error_message):
    """
    Send a failure notification to MS Teams.
    
    Args:
        error_message: Description of the error
    """
    if not is_enabled():
        return False
    
    title = "❌ File Export Failed!"
    message = f"**Error:** {error_message}"
    return send_teams_message(title, message, color="DC3545")  # Red
