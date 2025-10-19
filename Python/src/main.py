#!/usr/bin/env python3
"""
Main application entry point for the Hacktoberfest 2025 Project Tracker.
"""

import argparse
import sys
import os
from typing import Optional

from Contribute_Checker import ProjectTracker, Contributor


def main():
    """Main application function with CLI interface."""
    parser = argparse.ArgumentParser(
        description="Hacktoberfest 2025 Project Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --web                                               # Launch web interface
  python main.py --add-contributor "John Doe" johndoe john@example.com
  python main.py --add-contribution johndoe "my-repo" "bug-fix" "Fixed login issue" --pr 123
  python main.py --stats
  python main.py --leaderboard
  python main.py --interactive                                       # Interactive CLI mode
        """
    )
    
    # Add contributor arguments
    parser.add_argument(
        "--add-contributor",
        nargs=3,
        metavar=("NAME", "USERNAME", "EMAIL"),
        help="Add a new contributor (name, github_username, email)"
    )
    
    # Add contribution arguments
    parser.add_argument(
        "--add-contribution",
        nargs=4,
        metavar=("USERNAME", "REPO", "TYPE", "DESCRIPTION"),
        help="Add a contribution (github_username, repo_name, type, description)"
    )
    
    parser.add_argument(
        "--pr",
        type=int,
        help="Pull request number (use with --add-contribution)"
    )
    
    # Display options
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show project statistics"
    )
    
    parser.add_argument(
        "--leaderboard",
        action="store_true",
        help="Show contributor leaderboard"
    )
    
    parser.add_argument(
        "--list-contributors",
        action="store_true",
        help="List all contributors"
    )
    
    parser.add_argument(
        "--contributor-info",
        metavar="USERNAME",
        help="Show detailed info for a specific contributor"
    )
    
    # Interactive mode
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    # Email notification options
    parser.add_argument(
        "--enable-notifications",
        action="store_true",
        help="Enable email notifications for contributors"
    )
    
    parser.add_argument(
        "--notify-contributor",
        metavar="USERNAME",
        help="Send a notification email to a specific contributor"
    )
    
    parser.add_argument(
        "--notify-all",
        action="store_true",
        help="Send notification emails to all contributors"
    )
    
    parser.add_argument(
        "--notification-history",
        action="store_true",
        help="Show notification history"
    )
    
    parser.add_argument(
        "--smtp-server",
        metavar="SERVER",
        help="SMTP server address (e.g., smtp.gmail.com)"
    )
    
    parser.add_argument(
        "--sender-email",
        metavar="EMAIL",
        help="Email address to send from"
    )
    
    parser.add_argument(
        "--sender-password",
        metavar="PASSWORD",
        help="Email password (or use environment variable SENDER_PASSWORD)"
    # Web UI mode
    parser.add_argument(
        "--web",
        action="store_true",
        help="Launch the web user interface"
    )
    
    args = parser.parse_args()
    
    # Initialize the project tracker
    tracker = ProjectTracker()
    
    # Handle email notification setup
    if args.enable_notifications:
        smtp_server = args.smtp_server
        sender_email = args.sender_email
        sender_password = args.sender_password
        
        if not sender_email:
            print("❌ Error: --sender-email is required to enable notifications")
            return
        
        tracker.enable_email_notifications(smtp_server, sender_email, sender_password)
    
    # Handle different command line options
    if args.add_contributor:
        name, username, email = args.add_contributor
        contributor = tracker.add_contributor(name, username, email)
        print(f"✅ Added contributor: {contributor}")
    
    elif args.add_contribution:
        username, repo, contrib_type, description = args.add_contribution
        pr_number = args.pr
        
        success = tracker.add_contribution(username, repo, contrib_type, description, pr_number)
        if success:
            contributor = tracker.get_contributor(username)
            print(f"✅ Added contribution for {contributor.name}")
            print(f"   Repository: {repo}")
            print(f"   Type: {contrib_type}")
            print(f"   Description: {description}")
            if pr_number:
                print(f"   PR Number: #{pr_number}")
        else:
            print(f"❌ Error: Contributor '{username}' not found. Add them first!")
    
    elif args.stats:
        tracker.print_stats()
    
    elif args.leaderboard:
        tracker.print_leaderboard()
    
    elif args.list_contributors:
        contributors = tracker.get_all_contributors()
        if contributors:
            print(f"\n👥 All Contributors ({len(contributors)}) 👥")
            print("=" * 50)
            for contributor in contributors:
                print(f"  {contributor}")
        else:
            print("No contributors found!")
    
    elif args.contributor_info:
        contributor = tracker.get_contributor(args.contributor_info)
        if contributor:
            print(f"\n👤 {contributor.name} (@{contributor.github_username}) 👤")
            print("=" * 50)
            print(f"Email: {contributor.email or 'Not provided'}")
            print(f"Joined: {contributor.joined_date.strftime('%Y-%m-%d')}")
            print(f"Total Contributions: {contributor.get_contribution_count()}")
            print(f"Hacktoberfest Status: {'✅ Complete' if contributor.is_hacktoberfest_complete() else '📝 In Progress'}")
            
            if contributor.contributions:
                print(f"\nContributions:")
                for i, contrib in enumerate(contributor.contributions, 1):
                    print(f"  {i}. {contrib['repo_name']} - {contrib['type']}")
                    print(f"     {contrib['description']}")
                    if contrib.get('pr_number'):
                        print(f"     PR: #{contrib['pr_number']}")
                    print(f"     Date: {contrib['date'][:10]}")
                    print()
        else:
            print(f"❌ Contributor '{args.contributor_info}' not found!")
    
    elif args.web:
        print("🎃 Launching Hacktoberfest 2025 Web UI...")
        try:
            import subprocess
            import sys
            subprocess.run([sys.executable, "run_web_ui.py"], cwd=os.path.dirname(__file__))
        except Exception as e:
            print(f"Error launching web UI: {e}")
            print("Try running: python src/run_web_ui.py")
    
    elif args.interactive:
        interactive_mode(tracker)
    
    elif args.notify_contributor:
        success = tracker.send_notification_to_contributor(args.notify_contributor)
        if not success:
            sys.exit(1)
    
    elif args.notify_all:
        results = tracker.send_notifications_to_all_contributors()
        if results:
            successful = sum(1 for v in results.values() if v)
            print(f"\n✅ Sent {successful}/{len(results)} notifications successfully")
        else:
            print("❌ No contributors to notify or notifications not enabled")
    
    elif args.notification_history:
        history = tracker.get_notification_history()
        if history:
            print("\n📧 Notification History 📧")
            print("=" * 70)
            for record in history:
                print(f"Recipient: {record.get('recipient', 'N/A')}")
                print(f"Username: {record.get('username', 'N/A')}")
                print(f"Status: {record.get('status', 'N/A')}")
                print(f"Timestamp: {record.get('timestamp', 'N/A')}")
                if 'milestone' in record:
                    print(f"Milestone: {record['milestone']} contributions")
                print("-" * 70)
        else:
            print("No notification history found.")
    
    else:
        # Default behavior - show welcome message and basic stats
        print("🎃 Welcome to Hacktoberfest 2025 Project Tracker! 🎃")
        print()
        tracker.print_stats()
        print()
        print("Use --help to see available commands or --interactive for interactive mode.")


def interactive_mode(tracker: ProjectTracker):
    """Run the application in interactive mode."""
    print("\n🎃 Hacktoberfest 2025 - Interactive Mode 🎃")
    print("Type 'help' for available commands or 'quit' to exit.")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "quit" or command == "exit":
                print("Goodbye! Happy Hacktoberfest! 🎃")
                break
            
            elif command == "help":
                print_help()
            
            elif command == "stats":
                tracker.print_stats()
            
            elif command == "leaderboard":
                tracker.print_leaderboard()
            
            elif command == "list":
                contributors = tracker.get_all_contributors()
                if contributors:
                    print(f"\n👥 All Contributors ({len(contributors)}) 👥")
                    for contributor in contributors:
                        print(f"  {contributor}")
                else:
                    print("No contributors found!")
            
            elif command.startswith("add contributor"):
                add_contributor_interactive(tracker)
            
            elif command.startswith("add contribution"):
                add_contribution_interactive(tracker)
            
            elif command.startswith("info"):
                parts = command.split()
                if len(parts) >= 2:
                    username = parts[1]
                    show_contributor_info(tracker, username)
                else:
                    print("Usage: info <github_username>")
            
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! Happy Hacktoberfest! 🎃")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_help():
    """Print help for interactive mode."""
    print("""
Available commands:
  stats                 - Show project statistics
  leaderboard          - Show contributor leaderboard
  list                 - List all contributors
  add contributor      - Add a new contributor (interactive)
  add contribution     - Add a contribution (interactive)
  info <username>      - Show detailed info for a contributor
  help                 - Show this help message
  quit/exit           - Exit the program
    """)


def add_contributor_interactive(tracker: ProjectTracker):
    """Interactive contributor addition."""
    try:
        name = input("Enter full name: ").strip()
        username = input("Enter GitHub username: ").strip()
        email = input("Enter email (optional): ").strip()
        
        if not name or not username:
            print("Name and GitHub username are required!")
            return
        
        contributor = tracker.add_contributor(name, username, email)
        print(f"✅ Added contributor: {contributor}")
    except Exception as e:
        print(f"Error adding contributor: {e}")


def add_contribution_interactive(tracker: ProjectTracker):
    """Interactive contribution addition."""
    try:
        username = input("Enter GitHub username: ").strip()
        repo = input("Enter repository name: ").strip()
        contrib_type = input("Enter contribution type (bug-fix/feature/documentation/etc): ").strip()
        description = input("Enter description: ").strip()
        pr_input = input("Enter PR number (optional): ").strip()
        
        if not all([username, repo, contrib_type, description]):
            print("Username, repository, type, and description are required!")
            return
        
        pr_number = None
        if pr_input:
            try:
                pr_number = int(pr_input)
            except ValueError:
                print("Invalid PR number, ignoring...")
        
        success = tracker.add_contribution(username, repo, contrib_type, description, pr_number)
        if success:
            contributor = tracker.get_contributor(username)
            print(f"✅ Added contribution for {contributor.name}")
        else:
            print(f"❌ Error: Contributor '{username}' not found. Add them first!")
    except Exception as e:
        print(f"Error adding contribution: {e}")


def show_contributor_info(tracker: ProjectTracker, username: str):
    """Show detailed contributor information."""
    contributor = tracker.get_contributor(username)
    if contributor:
        print(f"\n👤 {contributor.name} (@{contributor.github_username}) 👤")
        print(f"Email: {contributor.email or 'Not provided'}")
        print(f"Joined: {contributor.joined_date.strftime('%Y-%m-%d')}")
        print(f"Total Contributions: {contributor.get_contribution_count()}")
        print(f"Hacktoberfest Status: {'✅ Complete' if contributor.is_hacktoberfest_complete() else '📝 In Progress'}")
        
        if contributor.contributions:
            print(f"\nRecent Contributions:")
            for contrib in contributor.contributions[-3:]:  # Show last 3
                print(f"  • {contrib['repo_name']} - {contrib['type']}")
                print(f"    {contrib['description']}")
    else:
        print(f"❌ Contributor '{username}' not found!")


if __name__ == "__main__":
    main()