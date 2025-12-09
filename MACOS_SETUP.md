# macOS Setup Guide

This guide covers macOS-specific setup and considerations for the File Location Exporter.

## Installation

### 1. Install Python (if not already installed)

Check if Python 3 is installed:
```bash
python3 --version
```

If not installed, download from: https://www.python.org/downloads/macos/

Or install via Homebrew:
```bash
brew install python3
```

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

Or install individually:
```bash
pip3 install pandas openpyxl python-docx python-pptx requests python-dotenv
```

### 3. Fix SSL Certificate Issues (if needed)

If you get SSL certificate errors:
```bash
/Applications/Python\ 3.*/Install\ Certificates.command
```

Or:
```bash
pip3 install --upgrade certifi
```

## Running the Application

### GUI Mode (Recommended)
```bash
python3 file_exporter.py
```

### Make it Executable (Optional)
```bash
chmod +x file_exporter.py
./file_exporter.py
```

## Email Configuration for macOS

### iCloud Mail (Recommended for Mac users)

1. **Generate App-Specific Password**:
   - Go to: https://appleid.apple.com
   - Sign in → Security section
   - Click "Generate Password" under App-Specific Passwords
   - Label it "File Exporter"
   - Copy the generated password

2. **Update .env file**:
   ```bash
   nano .env
   ```
   
   Add:
   ```
   SMTP_SERVER=smtp.mail.me.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@icloud.com
   SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx
   FROM_EMAIL=your-email@icloud.com
   TO_EMAIL=your-email@icloud.com
   ```

3. **Save and exit**: Press `Ctrl+X`, then `Y`, then `Enter`

### Gmail on macOS

Same as other platforms - see [SETUP_EMAIL.md](SETUP_EMAIL.md)

## Network Drive Considerations

### SMB/CIFS Shares (Common on Mac)

The application automatically detects network drives including:
- SMB shares (smb://server/share)
- AFP shares (afp://server/share)
- Mounted network volumes in /Volumes/

### Mounting Network Drives

**Via Finder**:
1. Finder → Go → Connect to Server (⌘K)
2. Enter: `smb://server/share`
3. Mount the drive
4. Use the mounted path in the application

**Via Command Line**:
```bash
# Mount SMB share
mount -t smbfs //username@server/share /Volumes/ShareName

# Check mounted drives
mount | grep smbfs
```

### Network Performance

For network drives, the application will:
- Detect the network location automatically
- Apply throttling (10ms delays)
- Use smaller batch sizes
- Show warning dialog before scanning

## Firewall Settings

If email notifications aren't working:

1. **System Preferences** → **Security & Privacy** → **Firewall**
2. Click lock icon to make changes
3. Click **Firewall Options**
4. Ensure Python is allowed to accept incoming connections
5. Or click **+** and add Python

## Gatekeeper Issues

If macOS blocks the application:

1. **System Preferences** → **Security & Privacy** → **General**
2. Click "Open Anyway" for the blocked application
3. Or run: `xattr -d com.apple.quarantine file_exporter.py`

## Creating a macOS App Bundle (Optional)

To create a double-clickable application:

### Using py2app

1. **Install py2app**:
   ```bash
   pip3 install py2app
   ```

2. **Create setup file**:
   ```bash
   py2applet --make-setup file_exporter.py
   ```

3. **Build app**:
   ```bash
   python3 setup.py py2app
   ```

4. **Find app**: `dist/file_exporter.app`

### Using PyInstaller (Alternative)

```bash
pip3 install pyinstaller
pyinstaller --onefile --windowed --name "File Exporter" file_exporter.py
```

App will be in `dist/` folder.

## Troubleshooting

### "Python is not installed as a framework"

If using tkinter with certain Python installations:
```bash
# Install Python from python.org (not Homebrew)
# Or use pythonw instead of python3
pythonw file_exporter.py
```

### "Module not found" errors

Make sure you're using the correct Python:
```bash
# Check which Python
which python3

# Check installed packages
pip3 list

# Reinstall if needed
pip3 install -r requirements.txt
```

### Permission Denied on Network Drives

```bash
# Check permissions
ls -la /Volumes/YourNetworkDrive

# Remount with proper credentials
# Unmount first
umount /Volumes/YourNetworkDrive

# Mount with credentials
mount -t smbfs //username:password@server/share /Volumes/YourNetworkDrive
```

### SSL Certificate Errors

```bash
# Update certificates
pip3 install --upgrade certifi

# Or run the certificate installer
/Applications/Python\ 3.*/Install\ Certificates.command
```

### Slow Performance on Network Drives

This is normal and expected. The application:
- Throttles requests to prevent network overload
- Uses smaller batch sizes
- Adds delays between operations

For better performance:
- Copy files to local drive first
- Scan during off-peak hours
- Use wired connection instead of WiFi

## Environment Variables

### View current .env settings:
```bash
cat .env
```

### Edit .env file:
```bash
nano .env
# or
open -e .env
# or
vim .env
```

## Testing

Test notifications:
```bash
python3 test_notifications.py
```

Test with small directory first:
```bash
python3 file_exporter.py
# Then select a small folder with ~100 files
```

## Uninstallation

Remove the application:
```bash
# Remove files
rm -rf /path/to/file_exporter/

# Remove Python packages (optional)
pip3 uninstall pandas openpyxl python-docx python-pptx requests python-dotenv
```

## Platform-Specific Features

| Feature | Status | Notes |
|---------|--------|-------|
| GUI | ✅ | Uses tkinter (built-in) |
| Network Detection | ✅ | Detects SMB/AFP/NFS |
| Email | ✅ | Works with all providers |
| Teams | ✅ | Requires internet |
| File Dates | ✅ | Uses st_birthtime on macOS |
| Office Metadata | ✅ | Requires openpyxl/docx/pptx |

## Performance Tips

1. **Use SSD**: Faster than HDD for local scans
2. **Wired Network**: Better than WiFi for network drives
3. **Close Other Apps**: Free up system resources
4. **Scan Off-Peak**: Less network congestion
5. **Filter Extensions**: Scan only needed file types

## Support

For macOS-specific issues:
1. Check console output for errors
2. Verify Python version: `python3 --version`
3. Check installed packages: `pip3 list`
4. Review system logs: Console.app
5. Test with local directory first

## Additional Resources

- Python for macOS: https://www.python.org/downloads/macos/
- Homebrew: https://brew.sh/
- py2app: https://py2app.readthedocs.io/
- PyInstaller: https://pyinstaller.org/
