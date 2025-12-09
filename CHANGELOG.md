# Changelog

## Version 2.0 - Network Safe with Notifications

### Major Features Added

#### Email Notifications
- ✅ Send email on export success with file count and output path
- ✅ Send email on export failure with detailed error message
- ✅ HTML formatted emails with color coding (green/red)
- ✅ Works on Windows, macOS, and Linux
- ✅ Supports Gmail, Outlook, Yahoo, iCloud, and custom SMTP
- ✅ Secure configuration via .env file

#### MS Teams Notifications
- ✅ Send Teams messages on success/failure
- ✅ Formatted cards with color coding
- ✅ Webhook-based (no authentication needed)
- ✅ Optional - can be used with or without email

#### Network Drive Safety
- ✅ Automatic network drive detection (UNC paths and mapped drives)
- ✅ Warning dialog before scanning network locations
- ✅ Throttled file access (10ms delays on network drives)
- ✅ Smaller batch sizes for network operations
- ✅ Error recovery and retry logic
- ✅ Connection monitoring (stops after 10 consecutive errors)
- ✅ Graceful degradation with partial results
- ✅ Timeout protection on all file operations

#### Cross-Platform Support
- ✅ Full Windows support
- ✅ Full macOS support (including iCloud email)
- ✅ Linux compatible
- ✅ Platform-specific documentation

### Enhanced Error Handling
- ✅ File-level error recovery (skip and continue)
- ✅ Network timeout handling
- ✅ Permission error handling
- ✅ Connection error detection
- ✅ Detailed error logging to console
- ✅ Error count reporting

### Security Improvements
- ✅ .gitignore prevents credential commits
- ✅ .env.example template for sharing
- ✅ App-specific password support
- ✅ Secure SMTP with TLS/SSL

### Documentation
- ✅ README.md - Quick start guide
- ✅ SETUP_EMAIL.md - Email configuration for all providers
- ✅ SETUP_TEAMS.md - Teams webhook setup
- ✅ NETWORK_SAFETY.md - Network drive safety features
- ✅ MACOS_SETUP.md - macOS-specific instructions
- ✅ CHANGELOG.md - Version history

### Testing Tools
- ✅ test_notifications.py - Test email and Teams setup

### Files Modified
- `file_exporter.py` - Added notification calls and network warnings
- `file_exporter_core.py` - Added network safety features
- `.env` - Added email configuration
- `.env.example` - Added email configuration template

### Files Added
- `email_notifier.py` - Email notification module
- `teams_notifier.py` - Teams notification module (renamed from sms_notifier.py)
- `.gitignore` - Prevents credential commits
- `requirements.txt` - All dependencies
- `test_notifications.py` - Notification testing tool
- `README.md` - Main documentation
- `SETUP_EMAIL.md` - Email setup guide
- `SETUP_TEAMS.md` - Teams setup guide
- `NETWORK_SAFETY.md` - Network safety documentation
- `MACOS_SETUP.md` - macOS setup guide
- `CHANGELOG.md` - This file

### Breaking Changes
- None - all changes are backward compatible
- Old installations will work without notifications if .env is not configured

### Migration from Version 1.0
1. Pull latest code
2. Run: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. Configure email/Teams settings in `.env`
5. Run `python test_notifications.py` to verify setup

## Version 1.0 - Original Release

### Features
- Directory scanning
- Excel export
- Folder structure breakdown
- File metadata extraction
- Office document author extraction
- Progress tracking
- Cancel functionality
- Extension filtering
- Title case conversion
