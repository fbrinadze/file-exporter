# File Location Exporter

A network-safe desktop application that scans directories and exports file information to Excel with email and Teams notifications.

## Quick Start

### For End Users
1. Run `File_Exporter.exe`
2. Select a directory
3. Click "Export to Excel"
4. Done!

### For Developers
```bash
pip install -r requirements.txt
python file_exporter.py
```

## Features

✅ Network drive safe with throttling and error recovery  
✅ Email notifications (configure in Settings)  
✅ MS Teams notifications (configure in Settings)  
✅ GUI settings dialog - no manual .env editing needed  
✅ Progress tracking with cancel option  
✅ Filter by file extensions  
✅ Extract file dates, types, and Office document authors  
✅ Duplicate file detection with detailed reports  
✅ Performance cache for faster repeat scans  
✅ Native dark mode support on macOS  
✅ Cross-platform (Windows, macOS, Linux)

## Configuration

Click the **⚙ Settings** button in the app to configure:
- Email notifications (SMTP settings)
- MS Teams notifications (webhook URL)

No manual file editing required!

## Building Executable

**Windows:**
```bash
build_exe.bat
```

**Manual:**
```bash
python -m PyInstaller --onefile --windowed file_exporter.py
```

The .exe will be in the `dist` folder.

## Distribution

The .exe works standalone - no Python installation needed!

To create a distribution package:
```bash
create_distribution.bat
```

## Documentation

See **[DOCUMENTATION.md](DOCUMENTATION.md)** for complete documentation including:
- Detailed setup instructions
- Email provider configurations
- Teams webhook setup
- Network drive safety features
- macOS-specific instructions
- Troubleshooting guide
- Technical details

## Requirements

### For Development
- Python 3.x
- pandas, openpyxl, python-docx, python-pptx
- requests, python-dotenv

### For End Users
- Windows 7+ or macOS 10.12+
- Nothing else!

## Files

- `file_exporter.py` - Main GUI application
- `file_exporter_core.py` - Core scanning logic
- `includes/` - Notification modules
  - `email_notifier.py` - Email notifications
  - `teams_notifier.py` - Teams notifications
- `build_exe.bat` - One-click executable builder
- `create_distribution.bat` - Package for distribution
- `test_notifications.py` - Test notification setup
- `DOCUMENTATION.md` - Complete documentation

## Support

1. Check [DOCUMENTATION.md](DOCUMENTATION.md)
2. Run `python test_notifications.py` to test notifications
3. Check console output for errors

## License

Free to use and modify.

---

**Version 2.2** | Network-Safe with Duplicate Detection & Dark Mode | Built with Python, tkinter, pandas, and openpyxl
