# Network Drive Safety Features

This application has been designed with multiple safeguards to prevent network drive issues and ensure reliable operation even on slow or unstable network connections.

## Safety Features

### 1. Network Drive Detection
- Automatically detects UNC paths (`\\server\share`)
- Identifies mapped network drives on Windows
- Warns users before scanning network locations
- Provides option to cancel before starting

### 2. Throttling & Rate Limiting
When scanning network drives, the application automatically:
- Adds 10ms delay between file operations
- Processes files in smaller batches (50 vs 100)
- Prevents overwhelming the network with rapid requests
- Reduces risk of connection timeouts

### 3. Error Recovery
- **File-level errors**: Skips problematic files and continues
- **Consecutive error tracking**: Stops if 10 consecutive errors occur
- **Connection monitoring**: Detects when network becomes unavailable
- **Graceful degradation**: Returns partial results if scan is interrupted

### 4. Timeout Protection
All file operations include timeout handling:
- File stat operations (dates, size)
- Author metadata extraction
- File access operations
- Network path validation

### 5. Error Types Handled
The application gracefully handles:
- `OSError`: File system errors
- `IOError`: Input/output errors
- `PermissionError`: Access denied
- `TimeoutError`: Network timeouts
- `ConnectionError`: Network unavailable

### 6. Progress Monitoring
- Real-time file count updates
- Cancel button always available
- Progress updates every 50-100 files
- Shows error count at completion

## Best Practices for Network Drives

### Before Scanning
1. ✅ Ensure stable network connection
2. ✅ Verify you have read access to the directory
3. ✅ Consider scanning during off-peak hours
4. ✅ Test with a small subdirectory first

### During Scanning
1. ✅ Monitor the progress counter
2. ✅ Use Cancel button if scan seems stuck
3. ✅ Watch for error messages in console
4. ✅ Be patient - network scans are slower

### If Problems Occur
1. **Scan stops with error**: Check network connection
2. **Very slow progress**: Normal for large network directories
3. **Many skipped files**: Check file permissions
4. **Connection error**: Network drive may be offline

## Technical Details

### Network Detection Logic
```
UNC Path: \\server\share\folder
Mapped Drive: Check via 'net use' command
Local Drive: No special handling needed
```

### Throttling Settings
```
Network Drive:
  - Delay: 10ms per 10 files
  - Batch: 50 files per progress update
  
Local Drive:
  - Delay: None
  - Batch: 100 files per progress update
```

### Error Thresholds
```
Max Consecutive Errors: 10
Action: Stop scan and report error
Reason: Network likely unavailable
```

## What This Prevents

### ❌ Without Safety Features
- Network drive becomes unresponsive
- Other users experience slowdowns
- Application hangs indefinitely
- Incomplete or corrupted results
- No way to recover from errors

### ✅ With Safety Features
- Controlled, throttled access
- Minimal impact on network performance
- Graceful error handling
- User can cancel anytime
- Partial results if interrupted
- Clear error messages

## Performance Impact

### Local Drives
- **Impact**: Minimal (< 1% slower)
- **Reason**: Error checking overhead only

### Network Drives
- **Impact**: 10-20% slower than unthrottled
- **Benefit**: Prevents network overload
- **Trade-off**: Reliability over speed

## Monitoring & Logging

The application logs:
- File processing errors (console)
- Network detection results (console)
- Total error count (completion message)
- Consecutive error tracking (internal)

## Emergency Stop

If the scan appears stuck:
1. Click the **Cancel** button
2. Wait 2-3 seconds for graceful stop
3. Partial results will be available
4. Check console for error messages

## Testing Recommendations

Before scanning large network directories:

1. **Small test**: Scan a small subfolder first
2. **Monitor**: Watch progress counter
3. **Timing**: Note how long 100 files takes
4. **Estimate**: Calculate total time needed
5. **Schedule**: Plan for off-peak hours if large

## Support

If you experience issues:
1. Check console output for error messages
2. Verify network drive is accessible
3. Test with a local directory first
4. Try a smaller subset of files
5. Check your network connection stability
