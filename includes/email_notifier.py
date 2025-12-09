"""
Email Notification Module
==========================
Sends email notifications for export success or failure.
Works on Windows, macOS, and Linux.

Requirements:
    - python-dotenv (pip install python-dotenv)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


def load_email_config():
    """
    Load email configuration from environment variables.
    
    Returns:
        dict: Configuration dictionary with email settings
        
    Raises:
        ValueError: If required environment variables are missing
    """
    load_dotenv()
    
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT', '587')
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
    
    if not all([smtp_server, smtp_username, smtp_password, from_email, to_email]):
        raise ValueError(
            "Missing email configuration. Please ensure .env file exists with:\n"
            "SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, FROM_EMAIL, TO_EMAIL"
        )
    
    return {
        'smtp_server': smtp_server,
        'smtp_port': int(smtp_port),
        'smtp_username': smtp_username,
        'smtp_password': smtp_password,
        'from_email': from_email,
        'to_email': to_email
    }


def send_email(subject, body_html, body_text=None, config=None):
    """
    Send an email using SMTP.
    
    Args:
        subject: Email subject line
        body_html: HTML body content
        body_text: Plain text alternative (optional)
        config: Optional config dict (if None, loads from environment)
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        if config is None:
            config = load_email_config()
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = config['from_email']
        msg['To'] = config['to_email']
        
        # Add plain text version
        if body_text:
            part1 = MIMEText(body_text, 'plain')
            msg.attach(part1)
        
        # Add HTML version
        part2 = MIMEText(body_html, 'html')
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()  # Secure the connection
            server.login(config['smtp_username'], config['smtp_password'])
            server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def is_enabled():
    """
    Check if email notifications are enabled.
    
    Returns:
        bool: True if enabled, False otherwise
    """
    load_dotenv()
    return os.getenv('EMAIL_ENABLED', 'false').lower() == 'true'


def send_success_notification(file_count, output_file):
    """
    Send a success notification email.
    
    Args:
        file_count: Number of files exported
        output_file: Path to the output Excel file
    """
    if not is_enabled():
        return False
    
    subject = "✅ File Export Complete"
    
    body_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <div style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 5px; padding: 20px; margin: 20px 0;">
          <h2 style="color: #155724; margin-top: 0;">✅ File Export Complete!</h2>
          <p style="color: #155724; font-size: 16px;">
            The file export has completed successfully.
          </p>
          <div style="background-color: white; padding: 15px; border-radius: 3px; margin: 15px 0;">
            <p style="margin: 5px 0;"><strong>Files Exported:</strong> {file_count}</p>
            <p style="margin: 5px 0;"><strong>Output File:</strong> {os.path.basename(output_file)}</p>
            <p style="margin: 5px 0; color: #666; font-size: 12px;"><em>Full path: {output_file}</em></p>
          </div>
          <p style="color: #155724; font-size: 14px; margin-bottom: 0;">
            The export completed without errors.
          </p>
        </div>
      </body>
    </html>
    """
    
    body_text = f"""
File Export Complete!

The file export has completed successfully.

Files Exported: {file_count}
Output File: {os.path.basename(output_file)}
Full path: {output_file}

The export completed without errors.
    """
    
    return send_email(subject, body_html, body_text)


def send_failure_notification(error_message):
    """
    Send a failure notification email.
    
    Args:
        error_message: Description of the error
    """
    if not is_enabled():
        return False
    
    subject = "❌ File Export Failed"
    
    body_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; padding: 20px; margin: 20px 0;">
          <h2 style="color: #721c24; margin-top: 0;">❌ File Export Failed!</h2>
          <p style="color: #721c24; font-size: 16px;">
            The file export encountered an error and could not complete.
          </p>
          <div style="background-color: white; padding: 15px; border-radius: 3px; margin: 15px 0;">
            <p style="margin: 5px 0;"><strong>Error Details:</strong></p>
            <pre style="background-color: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; color: #721c24;">{error_message}</pre>
          </div>
          <p style="color: #721c24; font-size: 14px; margin-bottom: 0;">
            Please check the error message above and try again.
          </p>
        </div>
      </body>
    </html>
    """
    
    body_text = f"""
File Export Failed!

The file export encountered an error and could not complete.

Error Details:
{error_message}

Please check the error message above and try again.
    """
    
    return send_email(subject, body_html, body_text)
