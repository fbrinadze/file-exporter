================================================================================
FILE LOCATION EXPORTER - DISTRIBUTION PACKAGE
================================================================================

QUICK START (No Setup Required)
--------------------------------
1. Run File_Exporter.exe
2. Select a directory to scan
3. Click "Export to Excel"
4. Choose where to save the file
5. Done!

The program works immediately without any installation or configuration.


OPTIONAL: Enable Email/Teams Notifications
-------------------------------------------
If you want to receive notifications when exports complete or fail:

1. Copy ".env.example" to ".env" (remove the .example)
2. Edit ".env" with Notepad
3. Add your email or Teams settings
4. Save and close

See SETUP_EMAIL.txt or SETUP_TEAMS.txt for detailed instructions.


WHAT'S INCLUDED
---------------
File_Exporter.exe       - The main application (this is all you need!)
.env.example            - Template for notification settings (optional)
SETUP_EMAIL.txt         - Email notification setup guide (optional)
SETUP_TEAMS.txt         - Teams notification setup guide (optional)
DISTRIBUTION_README.txt - This file


SYSTEM REQUIREMENTS
-------------------
- Windows 7 or later
- No Python installation required
- No other software required
- Works on any Windows computer


FEATURES
--------
✓ Scan any directory (local or network drives)
✓ Export file list to Excel
✓ Extract file dates and metadata
✓ Filter by file extensions
✓ Network drive safety features
✓ Progress tracking with cancel option
✓ Optional email notifications
✓ Optional Teams notifications


NETWORK DRIVES
--------------
The program automatically detects network drives and uses safe settings:
- Throttled file access
- Error recovery
- Connection monitoring

You'll see a warning before scanning network locations.


TROUBLESHOOTING
---------------
Problem: "Windows protected your PC" message
Solution: Click "More info" then "Run anyway"
         This is normal for new executables

Problem: Antivirus blocks the program
Solution: Add exception for File_Exporter.exe
         This is a false positive (common with PyInstaller)

Problem: Program crashes or won't start
Solution: Make sure you're on Windows 7 or later
         Try running as Administrator


SUPPORT
-------
For questions or issues, contact your IT department or the person who
provided this software.


VERSION INFORMATION
-------------------
Version: 2.0
Build Date: December 2025
Platform: Windows


================================================================================
