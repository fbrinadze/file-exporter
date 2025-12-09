# MS Teams Notification Setup Guide

## Prerequisites

1. **MS Teams Channel**: Access to a Teams channel where you can add webhooks
2. **Python packages**: Install required dependencies

## Installation Steps

### 1. Install Required Packages

```bash
pip install requests python-dotenv
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

### 2. Create an Incoming Webhook in MS Teams

1. Open MS Teams and navigate to the channel where you want to receive notifications
2. Click the **three dots (...)** next to the channel name
3. Select **Connectors** or **Workflows** (depending on your Teams version)
4. Search for **Incoming Webhook**
5. Click **Add** or **Configure**
6. Give your webhook a name (e.g., "File Exporter Notifications")
7. Optionally upload an icon
8. Click **Create**
9. **Copy the webhook URL** - you'll need this for the next step

### 3. Create Your .env File

1. Copy the example file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your webhook URL:
   ```
   TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/webhookb2/abc123...
   ```

   Paste the full webhook URL you copied from Teams.

### 4. Verify Setup

The `.env` file is automatically excluded from git by `.gitignore`, so your webhook URL will never be committed.

## Usage

Once configured, the application will automatically send Teams notifications:

- ✅ **Success**: When export completes successfully (includes file count and filename)
- ❌ **Failure**: When an error occurs during export (includes error message)

Messages appear as formatted cards in your Teams channel with color coding:
- Green for success
- Red for errors

## Troubleshooting

**Notifications not appearing in Teams?**
- Verify your webhook URL is correct and complete
- Check that the webhook is still active in Teams (it may have been removed)
- Ensure you have internet connectivity
- Check the console output for error messages
- Test the webhook URL manually using a tool like Postman

**Missing .env file?**
- Make sure you created `.env` (not `.env.txt`)
- Verify the file is in the same directory as `file_exporter.py`

**Webhook expired or removed?**
- Webhooks can be removed by Teams admins
- Create a new webhook following steps 2-3 above

## Security Notes

- ✅ `.env` is in `.gitignore` - your webhook URL is safe
- ✅ Never commit `.env` to version control
- ✅ Share `.env.example` with your team, not `.env`
- ✅ Each developer should create their own `.env` file
- ⚠️ Treat webhook URLs like passwords - anyone with the URL can post to your channel
