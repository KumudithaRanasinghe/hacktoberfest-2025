# 📧 Email Notification System - Setup Guide

## Overview

The Hacktoberfest 2025 Project Tracker now includes an advanced email notification system with JWT token generation for secure contributor communications.

## Features

✨ **Email Notifications:**
- 👋 Welcome emails for new contributors
- 🎊 Milestone achievement notifications
- 🏆 Hacktoberfest completion congratulations
- 🔐 JWT tokens for email verification
- 📊 Notification history tracking

## Setup Instructions

### 1. Install Dependencies

First, ensure you have PyJWT installed:

```bash
pip install -r requirements.txt
```

### 2. Configure Email Credentials

#### Option A: Using Environment Variables (Recommended)

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your email credentials:
```
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
JWT_SECRET=your-secure-secret-key
```

3. For **Gmail**, follow these steps:
   - Enable 2-Factor Authentication: https://myaccount.google.com/security
   - Generate an App Password: https://myaccount.google.com/apppasswords
   - Copy the 16-character app password to `SENDER_PASSWORD`

#### Option B: Command Line Arguments

Pass credentials directly via CLI:

```bash
python src/main.py --enable-notifications \
  --sender-email your-email@gmail.com \
  --sender-password your-app-password \
  --smtp-server smtp.gmail.com
```

### 3. Usage Examples

#### Enable Notifications and Add a Contributor

```bash
python src/main.py \
  --enable-notifications \
  --sender-email your-email@gmail.com \
  --sender-password your-app-password \
  --add-contributor "John Doe" johndoe john@example.com
```

A welcome email will automatically be sent to `john@example.com`.

#### Add a Contribution (Triggers Milestone Notification)

```bash
python src/main.py \
  --enable-notifications \
  --sender-email your-email@gmail.com \
  --add-contribution johndoe "my-repo" "bug-fix" "Fixed login issue" \
  --pr 123
```

A milestone notification will be sent when the contribution is added.

#### Send Notification to Specific Contributor

```bash
python src/main.py \
  --enable-notifications \
  --sender-email your-email@gmail.com \
  --notify-contributor johndoe
```

#### Send Notifications to All Contributors

```bash
python src/main.py \
  --enable-notifications \
  --sender-email your-email@gmail.com \
  --notify-all
```

#### View Notification History

```bash
python src/main.py --notification-history
```

#### Interactive Mode with Notifications

```bash
python src/main.py \
  --enable-notifications \
  --sender-email your-email@gmail.com \
  --interactive
```

## JWT Token Details

### Token Types

#### 1. Email Verification Token
```json
{
  "email": "contributor@example.com",
  "username": "githubuser",
  "type": "email_verification",
  "iat": 1697750000,
  "exp": 1697836400
}
```
- Expires in 24 hours (default)
- Used to verify contributor email addresses

#### 2. Milestone Token
```json
{
  "email": "contributor@example.com",
  "username": "githubuser",
  "milestone": 4,
  "type": "milestone",
  "iat": 1697750000,
  "exp": 1697923200
}
```
- Expires in 48 hours (default)
- Includes milestone/contribution count
- Unique for each achievement

### Token Verification

Use these methods in your code:

```python
from Contribute_Checker import EmailNotifier

notifier = EmailNotifier()

# Verify a token
is_valid, payload = notifier.verify_token(token_string)

if is_valid:
    print(f"Token valid for user: {payload['username']}")
else:
    print(f"Token error: {payload['error']}")
```

## Email Templates

### Welcome Email
Sent when a contributor is added. Includes:
- Welcome message
- Quick tips for Hacktoberfest
- Verification token
- Motivation and encouragement

### Milestone Email
Sent when a contribution is added. Includes:
- Contribution count update
- Progress bar toward 4 contributions
- Remaining contributions needed
- Milestone achievement token

### Completion Email
Sent when contributor reaches 4 contributions. Includes:
- Congratulations message
- Badge/achievement emoji
- List of accomplishments
- Completion token

## API Reference

### ProjectTracker Methods

```python
# Initialize with notifications
tracker = ProjectTracker(
    enable_notifications=True,
    smtp_server="smtp.gmail.com",
    sender_email="your-email@gmail.com",
    sender_password="your-app-password"
)

# Enable notifications after initialization
tracker.enable_email_notifications(
    smtp_server="smtp.gmail.com",
    sender_email="your-email@gmail.com",
    sender_password="your-app-password"
)

# Send notification to specific contributor
tracker.send_notification_to_contributor("githubuser")

# Send to all contributors
results = tracker.send_notifications_to_all_contributors()

# Get notification history
history = tracker.get_notification_history()
```

### EmailNotifier Methods

```python
from Contribute_Checker import EmailNotifier

notifier = EmailNotifier(
    smtp_server="smtp.gmail.com",
    sender_email="your-email@gmail.com",
    sender_password="your-app-password",
    jwt_secret="your-secret-key"
)

# Generate tokens
verification_token = notifier.generate_verification_token(
    email="user@example.com",
    username="githubuser",
    expires_in_hours=24
)

milestone_token = notifier.generate_milestone_token(
    email="user@example.com",
    username="githubuser",
    milestone=4,
    expires_in_hours=48
)

# Verify tokens
is_valid, payload = notifier.verify_token(verification_token)

# Send emails
success = notifier.send_welcome_email(
    recipient_email="user@example.com",
    name="John Doe",
    username="githubuser"
)

success = notifier.send_milestone_notification(
    recipient_email="user@example.com",
    username="githubuser",
    contribution_count=4,
    is_hacktoberfest_complete=True
)

# Get history
history = notifier.get_notification_history()
```

## Troubleshooting

### Email Not Sending

1. **Check email credentials**
   ```bash
   python -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587).starttls()"
   ```

2. **Verify environment variables are loaded**
   - Ensure `.env` file exists in the project root
   - Check that variables are set correctly

3. **Check SMTP settings**
   - Gmail: `smtp.gmail.com:587`
   - Outlook: `smtp-mail.outlook.com:587`
   - Yahoo: `smtp.mail.yahoo.com:587`

### JWT Token Issues

1. **Token verification fails**
   - Ensure `JWT_SECRET` is the same on generation and verification
   - Check if token has expired

2. **Invalid signature**
   - Token may have been modified
   - Ensure you're using the correct secret key

### Common Errors

**Error: "SMTP authentication failed"**
- Use an App Password (not regular password) for Gmail
- Ensure 2FA is enabled for Gmail

**Error: "Connection refused"**
- Check SMTP server address
- Verify SMTP port is correct (usually 587 for TLS)

## Security Best Practices

1. **Never commit `.env` file**
   - Add `.env` to `.gitignore`
   - Always use `.env.example` as template

2. **Use strong JWT secret**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Rotate credentials regularly**
   - Regenerate app passwords periodically
   - Update JWT secret if compromised

4. **Validate email addresses**
   - Verify email format before sending
   - Implement double opt-in if needed

## Advanced Usage

### Custom Email Templates

Modify the email template methods in `EmailNotifier`:

```python
# Override in your code
def custom_email_template(username, count):
    return f"""
    <html>
        <body>
            <h1>Hello {username}!</h1>
            <p>You have {count} contributions!</p>
        </body>
    </html>
    """
```

### Batch Processing

```python
# Send notifications to specific contributor group
completed = tracker.get_completed_contributors()
for contributor in completed:
    if contributor.email:
        tracker.send_notification_to_contributor(contributor.github_username)
```

### Notification Scheduling

```python
import schedule
import time

# Schedule daily notifications
schedule.every().day.at("09:00").do(
    tracker.send_notifications_to_all_contributors
)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Support

For issues or questions:
- Check the main `README.md`
- Review the `API.md` documentation
- Open an issue on GitHub

---

Happy Hacktoberfesting! 🎃🚀
