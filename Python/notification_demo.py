#!/usr/bin/env python3
"""
Demo script to test the notification system.
This script creates sample contributors and contributions to showcase the notification UI.
"""

import sys
import os
import time
from datetime import datetime, timedelta

# Add the parent directory to the path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from Contribute_Checker import ProjectTracker
from Contribute_Checker.notification_system import notification_manager, NotificationType, NotificationPriority


def main():
    """Main function to demonstrate notification system."""
    print("🎃 Hacktoberfest 2025 Notification System Demo")
    print("=" * 50)
    
    # Initialize project tracker
    tracker = ProjectTracker("Hacktoberfest 2025 Demo")
    
    # Create sample system notifications
    print("\n📢 Creating system notifications...")
    
    system_notifications = [
        {
            'title': '🎉 Hacktoberfest 2025 has begun!',
            'message': 'Welcome to Hacktoberfest 2025! Start making contributions to earn your place on the leaderboard.',
            'priority': NotificationPriority.HIGH
        },
        {
            'title': '⚠️ Maintenance Notice',
            'message': 'The system will undergo maintenance on Sunday from 2-4 AM EST. Please save your work.',
            'priority': NotificationPriority.NORMAL
        },
        {
            'title': '📊 Weekly Leaderboard Update',
            'message': 'Check out this week\'s top contributors! The competition is heating up.',
            'priority': NotificationPriority.LOW
        }
    ]
    
    for notif in system_notifications:
        notification_id = notification_manager.create_system_notification(
            title=notif['title'],
            message=notif['message'],
            priority=notif['priority']
        )
        print(f"  ✅ Created system notification: {notif['title']}")
    
    # Create sample contributors
    print("\n👥 Creating sample contributors...")
    
    sample_contributors = [
        {'name': 'Alice Johnson', 'username': 'alice_dev', 'email': 'alice@example.com'},
        {'name': 'Bob Smith', 'username': 'bob_codes', 'email': 'bob@example.com'},
        {'name': 'Carol Williams', 'username': 'carol_contrib', 'email': 'carol@example.com'},
        {'name': 'David Brown', 'username': 'david_dev', 'email': 'david@example.com'},
        {'name': 'Eve Davis', 'username': 'eve_engineer', 'email': 'eve@example.com'}
    ]
    
    for contrib_data in sample_contributors:
        contributor = tracker.add_contributor(
            contrib_data['name'],
            contrib_data['username'],
            contrib_data['email']
        )
        
        # Create welcome notification
        notification_manager.create_welcome_notification(
            contrib_data['username'],
            contrib_data['name']
        )
        
        print(f"  ✅ Added contributor: {contrib_data['name']} (@{contrib_data['username']})")
    
    # Create sample contributions and milestone notifications
    print("\n🚀 Creating sample contributions and milestone notifications...")
    
    sample_contributions = [
        # Alice - 4 contributions (complete)
        {'username': 'alice_dev', 'repo': 'awesome-project', 'type': 'feature', 'desc': 'Added user authentication system'},
        {'username': 'alice_dev', 'repo': 'awesome-project', 'type': 'bug-fix', 'desc': 'Fixed memory leak in data processing'},
        {'username': 'alice_dev', 'repo': 'open-source-lib', 'type': 'documentation', 'desc': 'Updated API documentation'},
        {'username': 'alice_dev', 'repo': 'community-tools', 'type': 'testing', 'desc': 'Added comprehensive unit tests'},
        
        # Bob - 2 contributions
        {'username': 'bob_codes', 'repo': 'web-framework', 'type': 'feature', 'desc': 'Implemented REST API endpoints'},
        {'username': 'bob_codes', 'repo': 'database-tools', 'type': 'enhancement', 'desc': 'Optimized query performance'},
        
        # Carol - 3 contributions
        {'username': 'carol_contrib', 'repo': 'ui-components', 'type': 'feature', 'desc': 'Created responsive navigation component'},
        {'username': 'carol_contrib', 'repo': 'ui-components', 'type': 'bug-fix', 'desc': 'Fixed CSS styling issues'},
        {'username': 'carol_contrib', 'repo': 'design-system', 'type': 'documentation', 'desc': 'Added component usage examples'},
        
        # David - 1 contribution
        {'username': 'david_dev', 'repo': 'mobile-app', 'type': 'feature', 'desc': 'Implemented push notifications'},
        
        # Eve - 5 contributions (complete+)
        {'username': 'eve_engineer', 'repo': 'data-science', 'type': 'feature', 'desc': 'Added machine learning models'},
        {'username': 'eve_engineer', 'repo': 'data-science', 'type': 'refactoring', 'desc': 'Refactored data preprocessing pipeline'},
        {'username': 'eve_engineer', 'repo': 'analytics-dashboard', 'type': 'feature', 'desc': 'Created interactive charts'},
        {'username': 'eve_engineer', 'repo': 'analytics-dashboard', 'type': 'testing', 'desc': 'Added integration tests'},
        {'username': 'eve_engineer', 'repo': 'ml-toolkit', 'type': 'documentation', 'desc': 'Written comprehensive tutorials'},
    ]
    
    for i, contrib in enumerate(sample_contributions):
        success = tracker.add_contribution(
            contrib['username'],
            contrib['repo'],
            contrib['type'],
            contrib['desc'],
            pr_number=100 + i
        )
        
        if success:
            contributor = tracker.get_contributor(contrib['username'])
            contribution_count = contributor.get_contribution_count()
            is_complete = contribution_count >= 4
            
            # Create milestone notification
            notification_manager.create_milestone_notification(
                contrib['username'],
                contribution_count,
                is_complete
            )
            
            print(f"  ✅ Added contribution for @{contrib['username']}: {contrib['desc'][:50]}...")
            if is_complete and contribution_count == 4:
                print(f"    🏆 @{contrib['username']} completed Hacktoberfest!")
            elif contribution_count in [1, 2, 3]:
                print(f"    🌟 @{contrib['username']} reached {contribution_count} contributions!")
    
    # Create some custom notifications
    print("\n📝 Creating custom notifications...")
    
    custom_notifications = [
        {
            'username': 'alice_dev',
            'title': '🎖️ Achievement Unlocked: First Timer!',
            'message': 'Congratulations! You completed your first Hacktoberfest. Welcome to the community!',
            'type': NotificationType.ACHIEVEMENT,
            'priority': NotificationPriority.HIGH,
            'action_url': '/contributor/alice_dev',
            'action_text': 'View Profile'
        },
        {
            'username': 'bob_codes',
            'title': '💡 Tip: Diversify Your Contributions',
            'message': 'Try contributing to different types of projects to expand your skills!',
            'type': NotificationType.INFO,
            'priority': NotificationPriority.LOW,
            'action_url': '/leaderboard',
            'action_text': 'View Leaderboard'
        },
        {
            'username': 'carol_contrib',
            'title': '🔥 You\'re on fire!',
            'message': 'You\'re so close to completing Hacktoberfest! Just one more contribution to go.',
            'type': NotificationType.MILESTONE,
            'priority': NotificationPriority.NORMAL
        }
    ]
    
    for notif in custom_notifications:
        notification_id = notification_manager.create_notification(
            title=notif['title'],
            message=notif['message'],
            notification_type=notif['type'],
            priority=notif['priority'],
            username=notif['username'],
            action_url=notif.get('action_url'),
            action_text=notif.get('action_text')
        )
        print(f"  ✅ Created custom notification for @{notif['username']}: {notif['title']}")
    
    # Display statistics
    print("\n📊 Notification Statistics:")
    print("-" * 30)
    
    # Global stats
    global_stats = notification_manager.get_notification_stats()
    print(f"Total notifications: {global_stats['total']}")
    print(f"Unread notifications: {global_stats['unread']}")
    print(f"Achievement notifications: {global_stats['type_achievement']}")
    print(f"Milestone notifications: {global_stats['type_milestone']}")
    print(f"System notifications: {global_stats['type_system']}")
    
    # Per-user stats
    print("\n👤 Per-user notification counts:")
    for contrib_data in sample_contributors:
        username = contrib_data['username']
        user_notifications = notification_manager.get_user_notifications(username)
        unread_count = len([n for n in user_notifications if not n.read])
        print(f"  @{username}: {len(user_notifications)} total, {unread_count} unread")
    
    print(f"\n✨ Demo completed! Visit http://localhost:5000/notifications to see the UI.")
    print("🎯 You can also test the API endpoints:")
    print("   - GET /api/notifications?user=alice_dev")
    print("   - GET /api/notifications/stats")
    print("   - POST /api/notifications/create")


if __name__ == '__main__':
    main()