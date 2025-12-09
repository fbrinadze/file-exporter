"""
MS Teams Notification Module
=============================
Sends notifications to MS Teams channel via webhook.

Requirements:
    - requests (pip install requests)
    - python-dotenv (pip install python-dotenv)
"""

import os
import requests
from dotenv import load_dotenv


def load_teams_config():
    """
    Load MS Teams webhook URL from environment variables.
    
    Returns:
        str: Teams webhook URL
        
    Raises:
        ValueError: If webhook URL is missing
    """
    load_dotenv()
    
    webhook_url = os.getenv('TEAMS_WEBHOOK_URL')
    
    if not webhook_url:
        raise ValueError(
            "Missing Teams webhook URL. Please ensure .env file exists with:\n"
            "TEAMS_WEBHOOK_URL"
        )
    
    return webhook_url


def send_teams_message(title, message, color="0078D4", webhook_url=None):
    """
    Send a message to MS Teams using webhook.
    
    Args:
        title: Message title
        message: The message text to send
        color: Hex color for the message card (default: blue)
        webhook_url: Optional webhook URL (if None, loads from environment)
        
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


def is_enabled():
    """
    Check if Teams notifications are enabled.
    
    Returns:
        bool: True if enabled, False otherwise
    """
    load_dotenv()
    return os.getenv('TEAMS_ENABLED', 'false').lower() == 'true'


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
