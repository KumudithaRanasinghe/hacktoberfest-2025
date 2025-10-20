#!/usr/bin/env python3
"""
Demo script for the Achievement Badges System.

This script demonstrates the badge system functionality including:
- Earning different types of badges
- Updating badge progress
- Creating achievement notifications
- Badge system integration with the web UI
"""

import sys
import os
import time
import json
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Contribute_Checker.notification_system import notification_manager, NotificationType, NotificationPriority

class BadgeSystemDemo:
    """Demonstration of the Achievement Badges System."""
    
    def __init__(self):
        """Initialize the badge system demo."""
        self.badges_data = {
            'first-contribution': {
                'name': 'First Contribution',
                'description': 'Made your first contribution to Hacktoberfest!',
                'type': 'milestone',
                'requirements': {'contributions': 1}
            },
            'streak-master': {
                'name': 'Streak Master',
                'description': 'Maintained a 5-day contribution streak!',
                'type': 'achievement',
                'requirements': {'consecutive_days': 5}
            },
            'bug-hunter': {
                'name': 'Bug Hunter',
                'description': 'Found and fixed 3 bugs in different projects!',
                'type': 'specialization',
                'requirements': {'bug_fixes': 3}
            },
            'feature-creator': {
                'name': 'Feature Creator',
                'description': 'Implement 5 new features across projects',
                'type': 'specialization',
                'requirements': {'features': 5}
            },
            'documentation-guru': {
                'name': 'Documentation Guru',
                'description': 'Improve documentation in 10 repositories',
                'type': 'specialization',
                'requirements': {'documentation_improvements': 10}
            },
            'test-champion': {
                'name': 'Test Champion',
                'description': 'Add comprehensive tests to 5 projects',
                'type': 'specialization',
                'requirements': {'test_additions': 5}
            },
            'early-bird': {
                'name': 'Early Bird',
                'description': 'Start contributing in the first week of October',
                'type': 'time_limited',
                'requirements': {'start_date': '2024-10-01', 'end_date': '2024-10-07'}
            },
            'team-player': {
                'name': 'Team Player',
                'description': 'Collaborate on 3 different team projects',
                'type': 'collaboration',
                'requirements': {'team_projects': 3}
            },
            'milestone-achiever': {
                'name': 'Milestone Achiever',
                'description': 'Complete all 4 required Hacktoberfest PRs',
                'type': 'milestone',
                'requirements': {'prs': 4}
            },
            'hacktoberfest-hero': {
                'name': 'Hacktoberfest Hero',
                'description': 'Complete Hacktoberfest and earn 10+ badges',
                'type': 'ultimate',
                'requirements': {'badges_earned': 10, 'hacktoberfest_complete': True}
            },
            'super-contributor': {
                'name': 'Super Contributor',
                'description': 'Make 20+ contributions in one month',
                'type': 'achievement',
                'requirements': {'monthly_contributions': 20}
            },
            'mentor': {
                'name': 'Mentor',
                'description': 'Help 5 new contributors with their first PRs',
                'type': 'leadership',
                'requirements': {'mentored_contributors': 5}
            }
        }
        
        self.user_progress = {
            'username': 'demo_user',
            'earned_badges': ['first-contribution', 'streak-master', 'bug-hunter'],
            'progress': {
                'contributions': 8,
                'consecutive_days': 5,
                'bug_fixes': 3,
                'features': 2,
                'documentation_improvements': 1,
                'test_additions': 0,
                'team_projects': 1,
                'prs': 3,
                'badges_earned': 3,
                'monthly_contributions': 8,
                'mentored_contributors': 0,
            }
        }
    
    def demo_badge_earning(self):
        """Demonstrate earning a new badge."""
        print("🎯 Badge Earning Demo")
        print("=" * 50)
        
        # Simulate earning the Feature Creator badge
        badge_id = 'feature-creator'
        badge_info = self.badges_data[badge_id]
        
        print(f"📋 Current progress for '{badge_info['name']}': 2/5 features")
        print("💻 Simulating creation of 3 more features...")
        
        for i in range(3, 6):  # Complete the remaining features
            time.sleep(1)
            self.user_progress['progress']['features'] = i
            print(f"   ✅ Feature {i} implemented!")
            
            if i == 5:  # Badge earned!
                self.user_progress['earned_badges'].append(badge_id)
                self.user_progress['progress']['badges_earned'] += 1
                
                # Create achievement notification
                notification_id = notification_manager.create_notification(
                    title="🎉 Badge Earned!",
                    message=f"Congratulations! You've earned the {badge_info['name']} badge!",
                    notification_type=NotificationType.ACHIEVEMENT,
                    priority=NotificationPriority.HIGH,
                    username=self.user_progress['username'],
                    metadata={
                        'badge_id': badge_id,
                        'badge_name': badge_info['name'],
                        'earned_date': datetime.now().isoformat()
                    }
                )
                
                print(f"🏆 BADGE EARNED: {badge_info['name']}")
                print(f"📝 {badge_info['description']}")
                print(f"🔔 Notification created (ID: {notification_id})")
        
        print()
    
    def demo_progress_tracking(self):
        """Demonstrate progress tracking for multiple badges."""
        print("📊 Badge Progress Tracking Demo")
        print("=" * 50)
        
        progress_badges = [
            ('documentation-guru', 'documentation_improvements', 10),
            ('super-contributor', 'monthly_contributions', 20),
            ('milestone-achiever', 'prs', 4),
            ('mentor', 'mentored_contributors', 5)
        ]
        
        for badge_id, progress_key, target in progress_badges:
            badge_info = self.badges_data[badge_id]
            current = self.user_progress['progress'][progress_key]
            percentage = (current / target) * 100
            
            print(f"🎯 {badge_info['name']}")
            print(f"   Progress: {current}/{target} ({percentage:.1f}%)")
            print(f"   Status: {'✅ Earned' if badge_id in self.user_progress['earned_badges'] else '🔄 In Progress' if current > 0 else '🔒 Locked'}")
            print()
    
    def demo_badge_categories(self):
        """Demonstrate different badge categories."""
        print("🏷️ Badge Categories Demo")
        print("=" * 50)
        
        categories = {}
        for badge_id, badge_info in self.badges_data.items():
            category = badge_info['type']
            if category not in categories:
                categories[category] = []
            categories[category].append({
                'id': badge_id,
                'name': badge_info['name'],
                'earned': badge_id in self.user_progress['earned_badges']
            })
        
        for category, badges in categories.items():
            earned_count = sum(1 for badge in badges if badge['earned'])
            total_count = len(badges)
            
            print(f"📂 {category.replace('_', ' ').title()}: {earned_count}/{total_count} earned")
            for badge in badges:
                status = "✅" if badge['earned'] else "⭕"
                print(f"   {status} {badge['name']}")
            print()
    
    def demo_notification_integration(self):
        """Demonstrate integration with the notification system."""
        print("🔔 Notification Integration Demo")
        print("=" * 50)
        
        # Create different types of badge-related notifications
        notifications = [
            {
                'title': 'New Badge Available!',
                'message': 'You\'re close to earning the Documentation Guru badge. Add 9 more documentation improvements!',
                'type': NotificationType.INFO,
                'priority': NotificationPriority.NORMAL
            },
            {
                'title': 'Badge Progress Update',
                'message': 'Great job! You\'ve made progress on 3 different badges today.',
                'type': NotificationType.SUCCESS,
                'priority': NotificationPriority.LOW
            },
            {
                'title': 'Limited Time Badge!',
                'message': 'The Early Bird badge expires in 2 days. Start contributing now!',
                'type': NotificationType.WARNING,
                'priority': NotificationPriority.HIGH
            }
        ]
        
        created_notifications = []
        for notification in notifications:
            notification_id = notification_manager.create_notification(
                title=notification['title'],
                message=notification['message'],
                notification_type=notification['type'],
                priority=notification['priority'],
                username=self.user_progress['username']
            )
            created_notifications.append(notification_id)
            print(f"📨 Created notification: {notification['title']}")
        
        print(f"\n💡 Total notifications created: {len(created_notifications)}")
        
        # Show user notifications
        user_notifications = notification_manager.get_user_notifications(
            self.user_progress['username'], 
            unread_only=True
        )
        print(f"📬 Unread notifications for user: {len(user_notifications)}")
        
        return created_notifications
    
    def demo_badge_statistics(self):
        """Demonstrate badge statistics and analytics."""
        print("📈 Badge Statistics Demo")
        print("=" * 50)
        
        total_badges = len(self.badges_data)
        earned_badges = len(self.user_progress['earned_badges'])
        completion_rate = (earned_badges / total_badges) * 100
        
        print(f"🏆 Total Badges Available: {total_badges}")
        print(f"✅ Badges Earned: {earned_badges}")
        print(f"📊 Completion Rate: {completion_rate:.1f}%")
        print()
        
        # Badge type distribution
        type_stats = {}
        for badge_info in self.badges_data.values():
            badge_type = badge_info['type']
            type_stats[badge_type] = type_stats.get(badge_type, 0) + 1
        
        print("📂 Badge Distribution by Type:")
        for badge_type, count in type_stats.items():
            print(f"   {badge_type.replace('_', ' ').title()}: {count} badges")
        print()
        
        # Recent achievements
        print("🎉 Recent Achievements:")
        for badge_id in self.user_progress['earned_badges'][-3:]:  # Last 3 earned
            badge_info = self.badges_data[badge_id]
            print(f"   🏅 {badge_info['name']}: {badge_info['description']}")
    
    def run_complete_demo(self):
        """Run the complete badge system demonstration."""
        print("🎮 Achievement Badges System Demo")
        print("🎃 Hacktoberfest 2025 Project Tracker")
        print("=" * 60)
        print()
        
        try:
            # Run all demo sections
            self.demo_badge_statistics()
            print("\n" + "─" * 60 + "\n")
            
            self.demo_badge_categories()
            print("─" * 60 + "\n")
            
            self.demo_progress_tracking()
            print("─" * 60 + "\n")
            
            self.demo_badge_earning()
            print("─" * 60 + "\n")
            
            notification_ids = self.demo_notification_integration()
            print("\n" + "─" * 60 + "\n")
            
            # Final statistics after earning new badge
            self.demo_badge_statistics()
            
            print("\n" + "=" * 60)
            print("✨ Demo completed successfully!")
            print("🌐 Visit the web UI to see the badges in action:")
            print("   • Dashboard: http://localhost:5000/")
            print("   • Achievement Badges: http://localhost:5000/achievement-badges")
            print("   • Notifications: http://localhost:5000/notifications")
            print("   • Contributors: http://localhost:5000/contributors")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ Demo failed with error: {e}")
            return False
    
    def save_demo_data(self, filename="badge_system_demo_data.json"):
        """Save demo data to a JSON file."""
        demo_data = {
            'timestamp': datetime.now().isoformat(),
            'badges_data': self.badges_data,
            'user_progress': self.user_progress,
            'demo_results': {
                'total_badges': len(self.badges_data),
                'earned_badges': len(self.user_progress['earned_badges']),
                'completion_rate': (len(self.user_progress['earned_badges']) / len(self.badges_data)) * 100
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(demo_data, f, indent=2)
            print(f"💾 Demo data saved to {filename}")
        except Exception as e:
            print(f"❌ Failed to save demo data: {e}")


def main():
    """Main function to run the badge system demo."""
    print("🚀 Starting Achievement Badges System Demo...")
    print()
    
    # Create and run the demo
    demo = BadgeSystemDemo()
    success = demo.run_complete_demo()
    
    if success:
        # Save demo data
        demo.save_demo_data()
        
        print("\n🎯 Next Steps:")
        print("1. Start the web application: python src/web_ui/app.py")
        print("2. Open your browser to http://localhost:5000")
        print("3. Navigate to the Achievement Badges page")
        print("4. Explore the badge system and notifications")
        print("\n🔧 Development Notes:")
        print("• Badge data is currently hardcoded for demo purposes")
        print("• In production, badges would be stored in a database")
        print("• Badge progress would be calculated from real contribution data")
        print("• Notifications are integrated with the existing system")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())