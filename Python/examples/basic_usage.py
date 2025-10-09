"""
Basic usage example for the Hacktoberfest 2025 Project Tracker.

This example demonstrates the core functionality of the project tracker.
"""

from Contribute_Checker import ProjectTracker, Contributor


def main():
    """Main example function demonstrating basic usage."""
    print("🎃 Hacktoberfest 2025 Project Tracker - Basic Example 🎃\n")
    
    # Create a new project tracker
    tracker = ProjectTracker("Example Hacktoberfest Project")
    
    # Add some contributors
    print("📋 Adding contributors...")
    alice = tracker.add_contributor("Alice Johnson", "alice_codes", "alice@example.com")
    bob = tracker.add_contributor("Bob Smith", "bob_dev", "bob@example.com") 
    charlie = tracker.add_contributor("Charlie Brown", "charlie_py", "charlie@example.com")
    
    print(f"Added {len(tracker.get_all_contributors())} contributors")
    
    # Add contributions for Alice (she's very active!)
    print("\n🚀 Adding contributions for Alice...")
    tracker.add_contribution("alice_codes", "awesome-web-app", "bug-fix", "Fixed login authentication bug", 101)
    tracker.add_contribution("alice_codes", "python-utils", "feature", "Added data validation utilities", 102)
    tracker.add_contribution("alice_codes", "open-source-docs", "documentation", "Improved API documentation", 103)
    tracker.add_contribution("alice_codes", "ml-toolkit", "feature", "Implemented new clustering algorithm", 104)
    tracker.add_contribution("alice_codes", "web-scraper", "bug-fix", "Fixed timeout handling", 105)
    
    # Add contributions for Bob
    print("🚀 Adding contributions for Bob...")
    tracker.add_contribution("bob_dev", "react-components", "feature", "Created reusable button component", 201)
    tracker.add_contribution("bob_dev", "api-gateway", "bug-fix", "Fixed CORS configuration", 202)
    tracker.add_contribution("bob_dev", "testing-framework", "testing", "Added unit tests for core modules", 203)
    
    # Add contributions for Charlie
    print("🚀 Adding contributions for Charlie...")
    tracker.add_contribution("charlie_py", "data-pipeline", "refactoring", "Refactored ETL process", 301)
    tracker.add_contribution("charlie_py", "automation-scripts", "feature", "Added automated deployment script", 302)
    
    # Display project statistics
    print("\n" + "="*60)
    tracker.print_stats()
    
    # Display leaderboard
    print("\n" + "="*60)
    tracker.print_leaderboard()
    
    # Show individual contributor information
    print("\n" + "="*60)
    print("👤 Individual Contributor Details")
    print("="*60)
    
    for contributor in tracker.get_all_contributors():
        print(f"\n{contributor.name} (@{contributor.github_username})")
        print(f"  Total Contributions: {contributor.get_contribution_count()}")
        print(f"  Hacktoberfest Status: {'✅ Complete' if contributor.is_hacktoberfest_complete() else '📝 In Progress'}")
        
        if contributor.contributions:
            print("  Recent Contributions:")
            for contrib in contributor.contributions[-2:]:  # Show last 2
                print(f"    • {contrib['repo_name']}: {contrib['description']}")
    
    # Show contributions by type
    print("\n" + "="*60)
    print("📊 Contributions by Type")
    print("="*60)
    
    contribution_types = {}
    for contributor in tracker.get_all_contributors():
        for contrib in contributor.contributions:
            contrib_type = contrib['type']
            contribution_types[contrib_type] = contribution_types.get(contrib_type, 0) + 1
    
    for contrib_type, count in sorted(contribution_types.items()):
        print(f"  {contrib_type}: {count}")
    
    # Show completed vs in-progress contributors
    completed = tracker.get_completed_contributors()
    all_contributors = tracker.get_all_contributors()
    
    print(f"\n📈 Completion Summary:")
    print(f"  Completed Hacktoberfest: {len(completed)}")
    print(f"  Still in Progress: {len(all_contributors) - len(completed)}")
    print(f"  Completion Rate: {(len(completed) / len(all_contributors) * 100):.1f}%")
    
    print(f"\n🎉 Example completed! Data saved to contributors.json")


if __name__ == "__main__":
    main()