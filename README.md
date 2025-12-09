# File Location Exporter

A network-safe desktop application that scans directories and exports file information to Excel with MS Teams notifications.

## Features

✅ **Network Drive Safe** - Throttled access, error recovery, connection monitoring  
✅ **Email Notifications** - Success/failure alerts via email (works on Windows, macOS, Linux)  
✅ **MS Teams Notifications** - Optional webhook notifications  
✅ **Flexible Filtering** - Filter by file extensions  
✅ **Metadata Extraction** - File dates and Office document authors  
✅ **Progress Tracking** - Real-time updates with cancel option  
✅ **Folder Structure** - Breaks directory hierarchy into columns  
✅ **Cross-Platform** - Works on Windows, macOS, and Linux  

## Quick Start

### 1. Install Dependencies

**Windows:**
```bash
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

See [MACOS_SETUP.md](MACOS_SETUP.md) for macOS-specific instructions.

### 2. Configure Notifications (Optional)

**Email** (Recommended - works everywhere):  
See [SETUP_EMAIL.md](SETUP_EMAIL.md) for email setup.

**MS Teams** (Optional):  
See [SETUP_TEAMS.md](SETUP_TEAMS.md) for webhook setup.

### 3. Run Application

**Windows:**
```bash
python file_exporter.py
```
Or use the compiled `.exe` in the `dist` folder.

**macOS/Linux:**
```bash
python3 file_exporter.py
```

## Usage

1. **Select Directory**: Click Browse to choose folder to scan
2. **Configure Options**: Set folder columns, filters, metadata options
3. **Export**: Click "Export to Excel" and choose save location
4. **Monitor**: Watch progress counter and use Cancel if needed

## Network Drive Safety

The application automatically detects network drives and applies safety features:
- Throttled file access (10ms delays)
- Error recovery and retry logic
- Connection monitoring
- Graceful failure handling

See [NETWORK_SAFETY.md](NETWORK_SAFETY.md) for complete details.

## Files

- `file_exporter.py` - Main GUI application
- `file_exporter_core.py` - Core scanning logic
- `teams_notifier.py` - MS Teams integration
- `email_notifier.py` - Email notification integration
- `.env` - Your configuration (not in git)
- `.env.example` - Configuration template

## Security

Your Teams webhook URL is stored in `.env` which is excluded from git via `.gitignore`.

## Building Executable

**Windows:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed file_exporter.py
```
The `.exe` will be in the `dist` folder.

**macOS:**
```bash
pip3 install pyinstaller
pyinstaller --onefile --windowed --name "File Exporter" file_exporter.py
```
The `.app` will be in the `dist` folder.

See [MACOS_SETUP.md](MACOS_SETUP.md) for py2app alternative.

## Testing Notifications

Test your notification setup before running exports:
```bash
python test_notifications.py
```

## Troubleshooting

**Network drive slow?**  
- Normal - network scans are throttled for safety
- Try scanning during off-peak hours
- Test with small subfolder first

**Files being skipped?**  
- Check file permissions
- Look for error messages in console
- Some files may be locked or inaccessible

**Email notifications not working?**  
- Check SMTP settings in `.env`
- Use app-specific passwords (not regular passwords)
- Check spam folder
- See [SETUP_EMAIL.md](SETUP_EMAIL.md)

**Teams notifications not working?**  
- Verify webhook URL in `.env`
- Check internet connection
- See [SETUP_TEAMS.md](SETUP_TEAMS.md)

**macOS-specific issues?**  
- See [MACOS_SETUP.md](MACOS_SETUP.md)
- SSL certificate errors: Run certificate installer
- Permission issues: Check Firewall settings

## Requirements

- Python 3.x
- pandas
- openpyxl
- python-docx (optional - for Word authors)
- python-pptx (optional - for PowerPoint authors)
- requests (for Teams notifications)
- python-dotenv (for configuration)

## License

Free to use and modify.
