#!/usr/bin/env python3
"""
Example: Email Notification System
Demonstrates how to use the email notification features.
"""

from Contribute_Checker import ProjectTracker, EmailNotifier
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def example_1_basic_notifications():
    """Example 1: Basic email notifications setup"""
    print("\n" + "="*60)
    print("Example 1: Basic Email Notifications")
    print("="*60)
    
    # Create tracker with notifications enabled
    tracker = ProjectTracker(
        enable_notifications=True,
        smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        sender_email=os.getenv("SENDER_EMAIL"),
        sender_password=os.getenv("SENDER_PASSWORD")
    )
    
    # Add a contributor (welcome email sent automatically)
    contributor = tracker.add_contributor(
        name="Jane Smith",
        github_username="janesmith",
        email="jane@example.com"  # Replace with real email for testing
    )
    print(f"✅ Added contributor: {contributor}")


def example_2_milestones():
    """Example 2: Milestone notifications"""
    print("\n" + "="*60)
    print("Example 2: Milestone Notifications")
    print("="*60)
    
    tracker = ProjectTracker(
        enable_notifications=True,
        smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        sender_email=os.getenv("SENDER_EMAIL"),
        sender_password=os.getenv("SENDER_PASSWORD")
    )
    
    # Add contributor
    tracker.add_contributor(
        name="Bob Johnson",
        github_username="bobjohnson",
        email="bob@example.com"  # Replace with real email
    )
    
    # Add contributions (milestone notifications sent automatically)
    for i in range(1, 5):
        tracker.add_contribution(
            github_username="bobjohnson",
            repo_name=f"awesome-project-{i}",
            contribution_type="bug-fix" if i % 2 == 0 else "feature",
            description=f"Contribution #{i}: Improved awesome-project",
            pr_number=100 + i
        )
        print(f"✅ Added contribution #{i}")


def example_3_jwt_tokens():
    """Example 3: JWT token generation and verification"""
    print("\n" + "="*60)
    print("Example 3: JWT Token Generation & Verification")
    print("="*60)
    
    notifier = EmailNotifier(
        jwt_secret=os.getenv("JWT_SECRET", "your-secret-key")
    )
    
    # Generate verification token
    verification_token = notifier.generate_verification_token(
        email="user@example.com",
        username="testuser",
        expires_in_hours=24
    )
    print(f"Verification Token: {verification_token[:50]}...")
    
    # Verify token
    is_valid, payload = notifier.verify_token(verification_token)
    print(f"Token Valid: {is_valid}")
    print(f"Email: {payload.get('email')}")
    print(f"Username: {payload.get('username')}")
    print(f"Type: {payload.get('type')}")
    
    # Generate milestone token
    milestone_token = notifier.generate_milestone_token(
        email="user@example.com",
        username="testuser",
        milestone=4
    )
    print(f"\nMilestone Token: {milestone_token[:50]}...")
    
    is_valid, payload = notifier.verify_token(milestone_token)
    print(f"Token Valid: {is_valid}")
    print(f"Milestone: {payload.get('milestone')}")


def example_4_manual_notifications():
    """Example 4: Send manual notifications"""
    print("\n" + "="*60)
    print("Example 4: Manual Notifications")
    print("="*60)
    
    tracker = ProjectTracker(
        enable_notifications=True,
        smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        sender_email=os.getenv("SENDER_EMAIL"),
        sender_password=os.getenv("SENDER_PASSWORD")
    )
    
    # Add some contributors
    tracker.add_contributor("Alice Wilson", "alicew", "alice@example.com")
    tracker.add_contributor("Charlie Brown", "charlieb", "charlie@example.com")
    
    # Send notification to specific contributor
    print("\nSending notification to alicew...")
    tracker.send_notification_to_contributor("alicew")
    
    # Send to all contributors
    print("\nSending notifications to all contributors...")
    results = tracker.send_notifications_to_all_contributors()
    print(f"Sent to {len(results)} contributors")


def example_5_notification_history():
    """Example 5: View notification history"""
    print("\n" + "="*60)
    print("Example 5: Notification History")
    print("="*60)
    
    tracker = ProjectTracker(
        enable_notifications=True,
        smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        sender_email=os.getenv("SENDER_EMAIL"),
        sender_password=os.getenv("SENDER_PASSWORD")
    )
    
    # Add contributor and send notification
    tracker.add_contributor("Diana Prince", "dianaprincess", "diana@example.com")
    
    # Get and display history
    history = tracker.get_notification_history()
    if history:
        print("\nNotification History:")
        for record in history:
            print(f"  - {record['recipient']}: {record['status']}")
    else:
        print("No notifications sent yet")


def main():
    """Run all examples"""
    print("\n🎃 Email Notification System Examples 🎃")
    print("================================================")
    
    # Check if email is configured
    if not os.getenv("SENDER_EMAIL"):
        print("\n⚠️  WARNING: SENDER_EMAIL not configured")
        print("To use email notifications, set up your .env file:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your email credentials")
        print("  3. Run this script again")
        print("\n📧 Showing examples for JWT tokens (no email needed)...\n")
        example_3_jwt_tokens()
    else:
        print("\n📧 Email configured, running all examples...\n")
        # Uncomment examples to run them
        # example_1_basic_notifications()
        # example_2_milestones()
        # example_4_manual_notifications()
        # example_5_notification_history()
        
        # Always run this one
        example_3_jwt_tokens()
    
    print("\n✅ Examples complete!")
    print("\nFor more information, see: Python/docs/EMAIL_NOTIFICATIONS.md")


if __name__ == "__main__":
    main()
