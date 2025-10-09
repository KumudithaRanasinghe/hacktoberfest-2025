#!/usr/bin/env python3
"""
Simple demonstration of the Hacktoberfest 2025 Project Tracker.
This script shows basic functionality without requiring external dependencies.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Contribute_Checker import ProjectTracker, Contributor


def main():
    """Demonstrate basic functionality of the project tracker."""
    print("🎃 Hacktoberfest 2025 Project Tracker - Demo 🎃")
    print("=" * 60)
    
    # Create a new tracker for demo (using a different file)
    tracker = ProjectTracker("Demo Project", "demo_contributors.json")
    
    print("\n📝 Adding contributors...")
    
    # Add some demo contributors
    contributors_data = [
        ("Sarah Chen", "sarah_dev", "sarah@example.com"),
        ("Mike Rodriguez", "mike_codes", "mike@example.com"),
        ("Emily Davis", "emily_py", "emily@example.com"),
    ]
    
    for name, username, email in contributors_data:
        contributor = tracker.add_contributor(name, username, email)
        print(f"  ✅ Added: {contributor}")
    
    print("\n🔨 Adding contributions...")
    
    # Add contributions
    contributions = [
        ("sarah_dev", "web-dashboard", "bug-fix", "Fixed responsive design issue", 101),
        ("sarah_dev", "api-backend", "feature", "Added user authentication", 102),
        ("sarah_dev", "mobile-app", "documentation", "Updated API documentation", 103),
        ("sarah_dev", "data-pipeline", "testing", "Added integration tests", 104),
        ("mike_codes", "frontend-lib", "refactoring", "Improved component structure", 201),
        ("mike_codes", "automation-tool", "feature", "Added config validation", 202),
        ("emily_py", "ml-pipeline", "performance", "Optimized data processing", 301),
    ]
    
    for username, repo, contrib_type, description, pr in contributions:
        success = tracker.add_contribution(username, repo, contrib_type, description, pr)
        if success:
            print(f"  ✅ Added contribution: {repo} ({contrib_type}) by {username}")
    
    print("\n" + "=" * 60)
    
    # Show statistics
    tracker.print_stats()
    
    print()
    
    # Show leaderboard
    tracker.print_leaderboard()
    
    print("\n📊 Detailed Analysis:")
    print("=" * 60)
    
    # Show who completed Hacktoberfest
    completed = tracker.get_completed_contributors()
    in_progress = [c for c in tracker.get_all_contributors() if not c.is_hacktoberfest_complete()]
    
    print(f"\n🎉 Completed Hacktoberfest ({len(completed)}):")
    for contributor in completed:
        print(f"  🏆 {contributor.name} - {contributor.get_contribution_count()} contributions")
    
    print(f"\n📝 In Progress ({len(in_progress)}):")
    for contributor in in_progress:
        remaining = 4 - contributor.get_contribution_count()
        print(f"  📋 {contributor.name} - {contributor.get_contribution_count()}/4 ({remaining} more needed)")
    
    # Show project stats
    stats = tracker.get_project_stats()
    print(f"\n📈 Project Summary:")
    print(f"  Total Contributors: {stats['total_contributors']}")
    print(f"  Total Contributions: {stats['total_contributions']}")
    print(f"  Completion Rate: {stats['completion_rate']}")
    
    # Show contribution types breakdown
    print(f"\n🏷️  Contribution Types:")
    type_counts = {}
    for contributor in tracker.get_all_contributors():
        for contrib in contributor.contributions:
            contrib_type = contrib["type"]
            type_counts[contrib_type] = type_counts.get(contrib_type, 0) + 1
    
    for contrib_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {contrib_type}: {count}")
    
    # Show repository breakdown
    print(f"\n📁 Repository Activity:")
    repo_counts = {}
    for contributor in tracker.get_all_contributors():
        for contrib in contributor.contributions:
            repo_name = contrib["repo_name"]
            repo_counts[repo_name] = repo_counts.get(repo_name, 0) + 1
    
    for repo_name, count in sorted(repo_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {repo_name}: {count} contributions")
    
    print(f"\n✨ Demo completed! Data saved to demo_contributors.json")
    print(f"🎯 Try running: python src/main.py --interactive")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)