# Email Notification Setup Guide

This guide works for Windows, macOS, and Linux.

## Prerequisites

1. **Email account** with SMTP access
2. **Python packages**: Already included in requirements.txt

## Quick Setup by Email Provider

### Gmail (Recommended)

1. **Enable 2-Factor Authentication** on your Google account
2. **Create an App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Click "Generate"
   - Copy the 16-character password

3. **Update .env file**:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   FROM_EMAIL=your-email@gmail.com
   TO_EMAIL=where-to-send@example.com
   ```

### Outlook / Office 365

1. **Update .env file**:
   ```
   SMTP_SERVER=smtp.office365.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@outlook.com
   SMTP_PASSWORD=your-password
   FROM_EMAIL=your-email@outlook.com
   TO_EMAIL=where-to-send@example.com
   ```

### Yahoo Mail

1. **Generate App Password**:
   - Go to Account Security settings
   - Create app password for "Desktop app"

2. **Update .env file**:
   ```
   SMTP_SERVER=smtp.mail.yahoo.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@yahoo.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@yahoo.com
   TO_EMAIL=where-to-send@example.com
   ```

### iCloud Mail (macOS)

1. **Generate App-Specific Password**:
   - Go to: https://appleid.apple.com
   - Sign in and go to Security section
   - Generate app-specific password

2. **Update .env file**:
   ```
   SMTP_SERVER=smtp.mail.me.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@icloud.com
   SMTP_PASSWORD=your-app-specific-password
   FROM_EMAIL=your-email@icloud.com
   TO_EMAIL=where-to-send@example.com
   ```

### Custom SMTP Server

If you have a custom email server:
```
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=587
SMTP_USERNAME=your-username
SMTP_PASSWORD=your-password
FROM_EMAIL=sender@yourdomain.com
TO_EMAIL=recipient@example.com
```

## Installation Steps

### 1. Install Dependencies

Already included in requirements.txt:
```bash
pip install python-dotenv
```

### 2. Configure .env File

1. Copy the example file:
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. Edit `.env` with your email settings (see provider sections above)

### 3. Test Configuration

Run the program and trigger an export to test email delivery.

## Email Format

### Success Email
- **Subject**: ✅ File Export Complete
- **Content**: 
  - Number of files exported
  - Output file name and path
  - Success confirmation
- **Format**: HTML with green styling

### Failure Email
- **Subject**: ❌ File Export Failed
- **Content**:
  - Detailed error message
  - Error type and description
  - Troubleshooting hints
- **Format**: HTML with red styling

## Troubleshooting

### "Authentication failed"
- **Gmail**: Make sure you're using an App Password, not your regular password
- **All providers**: Verify username and password are correct
- **2FA enabled**: You must use app-specific passwords

### "Connection refused" or "Timeout"
- Check SMTP server address is correct
- Verify port number (usually 587 for TLS)
- Check firewall isn't blocking SMTP
- Try port 465 (SSL) if 587 doesn't work

### "Sender address rejected"
- Make sure FROM_EMAIL matches your SMTP_USERNAME
- Some providers require exact match

### Emails not arriving
- Check spam/junk folder
- Verify TO_EMAIL address is correct
- Check email provider's sent folder
- Look for bounce-back messages

### macOS Specific Issues

**"Certificate verify failed"**
- Run: `/Applications/Python\ 3.x/Install\ Certificates.command`
- Or install certificates: `pip install --upgrade certifi`

**Firewall blocking**
- System Preferences → Security & Privacy → Firewall
- Allow Python to make network connections

### Windows Specific Issues

**Antivirus blocking SMTP**
- Add Python to antivirus exceptions
- Temporarily disable to test

**Corporate network**
- May block outbound SMTP (port 587/465)
- Contact IT department
- May need to use internal SMTP server

## Security Notes

- ✅ `.env` is in `.gitignore` - credentials are safe
- ✅ Never commit `.env` to version control
- ✅ Use app-specific passwords, not account passwords
- ✅ Each user should create their own `.env` file
- ⚠️ App passwords have same access as regular passwords - keep them secure

## Multiple Recipients

To send to multiple email addresses, use comma separation:
```
TO_EMAIL=person1@example.com,person2@example.com,person3@example.com
```

Note: Current version sends to one recipient. For multiple recipients, modify `email_notifier.py`:
```python
to_email = os.getenv('TO_EMAIL')
msg['To'] = to_email  # Can be comma-separated
```

## Disabling Notifications

### Disable Email Only
Remove or comment out email settings in `.env`:
```
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# ...
```

### Disable Teams Only
Remove or comment out Teams webhook:
```
# TEAMS_WEBHOOK_URL=https://...
```

### Disable Both
Comment out all notification settings in `.env`

## Platform Compatibility

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Gmail | ✅ | ✅ | ✅ |
| Outlook | ✅ | ✅ | ✅ |
| Yahoo | ✅ | ✅ | ✅ |
| iCloud | ✅ | ✅ | ✅ |
| Custom SMTP | ✅ | ✅ | ✅ |

## Testing

To test email configuration without running full export:

```python
from email_notifier import send_success_notification
send_success_notification(100, "test_output.xlsx")
```

## Support

If you experience issues:
1. Check console output for error messages
2. Verify SMTP settings are correct
3. Test with a simple email client first
4. Check provider's SMTP documentation
5. Ensure app passwords are being used (not regular passwords)
