@echo off
echo ========================================
echo Creating Distribution Package
echo ========================================
echo.

REM Check if exe exists
if not exist "dist\File_Exporter.exe" (
    echo ERROR: File_Exporter.exe not found!
    echo Please build the executable first by running build_exe.bat
    echo.
    pause
    exit /b 1
)

REM Create distribution folder
echo Creating distribution folder...
if exist "File_Exporter_Distribution" rmdir /s /q "File_Exporter_Distribution"
mkdir "File_Exporter_Distribution"

REM Copy executable
echo Copying executable...
copy "dist\File_Exporter.exe" "File_Exporter_Distribution\"

REM Copy optional setup files
echo Copying setup files...
copy ".env.example" "File_Exporter_Distribution\"
copy "DISTRIBUTION_README.txt" "File_Exporter_Distribution\"

REM Create simplified setup guides
echo Creating setup guides...

REM Email setup
(
echo EMAIL NOTIFICATION SETUP
echo ========================
echo.
echo 1. Copy ".env.example" to ".env"
echo 2. Open ".env" with Notepad
echo 3. Fill in your email settings:
echo.
echo    For Gmail:
echo    SMTP_SERVER=smtp.gmail.com
echo    SMTP_PORT=587
echo    SMTP_USERNAME=your-email@gmail.com
echo    SMTP_PASSWORD=your-app-password
echo    FROM_EMAIL=your-email@gmail.com
echo    TO_EMAIL=your-email@gmail.com
echo.
echo    For Outlook:
echo    SMTP_SERVER=smtp.office365.com
echo    SMTP_PORT=587
echo    SMTP_USERNAME=your-email@outlook.com
echo    SMTP_PASSWORD=your-password
echo    FROM_EMAIL=your-email@outlook.com
echo    TO_EMAIL=your-email@outlook.com
echo.
echo 4. Save and close
echo 5. Place ".env" in the same folder as File_Exporter.exe
echo.
echo IMPORTANT: Use app-specific passwords, not your regular password!
echo.
echo Gmail App Password: https://myaccount.google.com/apppasswords
) > "File_Exporter_Distribution\SETUP_EMAIL.txt"

REM Teams setup
(
echo TEAMS NOTIFICATION SETUP
echo ========================
echo.
echo 1. Open MS Teams
echo 2. Go to the channel where you want notifications
echo 3. Click the three dots (...) next to the channel name
echo 4. Select "Connectors" or "Workflows"
echo 5. Search for "Incoming Webhook"
echo 6. Click "Add" or "Configure"
echo 7. Give it a name like "File Exporter"
echo 8. Click "Create"
echo 9. Copy the webhook URL
echo.
echo 10. Copy ".env.example" to ".env"
echo 11. Open ".env" with Notepad
echo 12. Paste your webhook URL:
echo.
echo     TEAMS_WEBHOOK_URL=https://your-webhook-url-here
echo.
echo 13. Save and close
echo 14. Place ".env" in the same folder as File_Exporter.exe
) > "File_Exporter_Distribution\SETUP_TEAMS.txt"

echo.
echo ========================================
echo Distribution Package Created!
echo ========================================
echo.
echo Location: File_Exporter_Distribution\
echo.
echo Contents:
echo   - File_Exporter.exe (main program)
echo   - DISTRIBUTION_README.txt (instructions)
echo   - .env.example (notification template)
echo   - SETUP_EMAIL.txt (email setup guide)
echo   - SETUP_TEAMS.txt (Teams setup guide)
echo.
echo You can now:
echo   1. Zip the "File_Exporter_Distribution" folder
echo   2. Share it with anyone
echo   3. They can run File_Exporter.exe immediately
echo   4. Notifications are optional (requires .env setup)
echo.
pause
