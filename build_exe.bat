@echo off
echo ========================================
echo Building File Exporter Executable
echo ========================================
echo.

echo Checking PyInstaller installation...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
) else (
    echo PyInstaller is already installed.
)

echo.
echo Building executable...
python -m PyInstaller --onefile --windowed --name "File_Exporter" file_exporter.py

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo The executable is located at:
echo   dist\File_Exporter.exe
echo.
echo You can now distribute this .exe file.
echo It includes all dependencies and does not require Python to be installed.
echo.
pause
