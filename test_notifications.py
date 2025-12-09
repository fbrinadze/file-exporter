"""
Test Notification Configuration
================================
Quick test script to verify email and Teams notifications are working.
Run this before using the main application.
"""

import sys

print("=" * 60)
print("Testing Notification Configuration")
print("=" * 60)

# Test Email
print("\n1. Testing Email Configuration...")
try:
    from email_notifier import send_success_notification as email_success
    print("   ✓ Email module loaded")
    
    print("   Sending test email...")
    result = email_success(100, "test_output.xlsx")
    
    if result:
        print("   ✓ Email sent successfully!")
        print("   → Check your inbox (and spam folder)")
    else:
        print("   ✗ Email failed to send")
        print("   → Check console output above for error details")
        print("   → See SETUP_EMAIL.md for troubleshooting")
        
except ImportError:
    print("   ⚠ Email module not available")
    print("   → Install: pip install python-dotenv")
except ValueError as e:
    print(f"   ⚠ Configuration error: {e}")
    print("   → Check your .env file settings")
    print("   → See SETUP_EMAIL.md for setup instructions")
except Exception as e:
    print(f"   ✗ Error: {e}")
    print("   → See SETUP_EMAIL.md for troubleshooting")

# Test Teams
print("\n2. Testing Teams Configuration...")
try:
    from teams_notifier import send_success_notification as teams_success
    print("   ✓ Teams module loaded")
    
    print("   Sending test message...")
    result = teams_success(100, "test_output.xlsx")
    
    if result:
        print("   ✓ Teams message sent successfully!")
        print("   → Check your Teams channel")
    else:
        print("   ✗ Teams message failed to send")
        print("   → Check console output above for error details")
        print("   → See SETUP_TEAMS.md for troubleshooting")
        
except ImportError:
    print("   ⚠ Teams module not available")
    print("   → Install: pip install requests python-dotenv")
except ValueError as e:
    print(f"   ⚠ Configuration error: {e}")
    print("   → Check your .env file settings")
    print("   → See SETUP_TEAMS.md for setup instructions")
except Exception as e:
    print(f"   ✗ Error: {e}")
    print("   → See SETUP_TEAMS.md for troubleshooting")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
print("\nIf both tests passed, your notifications are configured!")
print("If either failed, check the error messages and setup guides.")
print("\nSetup Guides:")
print("  - Email: SETUP_EMAIL.md")
print("  - Teams: SETUP_TEAMS.md")
