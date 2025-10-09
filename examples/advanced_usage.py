"""
Advanced usage example showing more complex features of the Project Tracker.

This example demonstrates custom workflows, data analysis, and advanced features.
"""

import json
from datetime import datetime, timedelta
from Contribute_Checker import ProjectTracker, Contributor


class AdvancedProjectTracker(ProjectTracker):
    """Extended version of ProjectTracker with additional analysis features."""
    
    def get_contributions_by_repo(self, repo_name: str):
        """Get all contributions for a specific repository."""
        repo_contributions = []
        for contributor in self.get_all_contributors():
            for contrib in contributor.contributions:
                if contrib["repo_name"] == repo_name:
                    repo_contributions.append({
                        "contributor": contributor.name,
                        "github_username": contributor.github_username,
                        **contrib
                    })
        return repo_contributions
    
    def get_daily_contribution_stats(self):
        """Get contribution statistics by day."""
        daily_stats = {}
        for contributor in self.get_all_contributors():
            for contrib in contributor.contributions:
                date = contrib["date"][:10]  # Extract YYYY-MM-DD
                daily_stats[date] = daily_stats.get(date, 0) + 1
        return daily_stats
    
    def get_repository_leaderboard(self):
        """Get repositories sorted by number of contributions."""
        repo_stats = {}
        for contributor in self.get_all_contributors():
            for contrib in contributor.contributions:
                repo_name = contrib["repo_name"]
                if repo_name not in repo_stats:
                    repo_stats[repo_name] = {
                        "contribution_count": 0,
                        "contributors": set(),
                        "types": {}
                    }
                repo_stats[repo_name]["contribution_count"] += 1
                repo_stats[repo_name]["contributors"].add(contributor.github_username)
                contrib_type = contrib["type"]
                repo_stats[repo_name]["types"][contrib_type] = repo_stats[repo_name]["types"].get(contrib_type, 0) + 1
        
        # Convert sets to counts for JSON serialization
        for repo in repo_stats:
            repo_stats[repo]["unique_contributors"] = len(repo_stats[repo]["contributors"])
            del repo_stats[repo]["contributors"]
        
        return sorted(repo_stats.items(), key=lambda x: x[1]["contribution_count"], reverse=True)
    
    def get_contributor_growth_over_time(self):
        """Get contributor growth statistics over time."""
        growth_data = {}
        for contributor in self.get_all_contributors():
            join_date = contributor.joined_date.strftime("%Y-%m-%d")
            growth_data[join_date] = growth_data.get(join_date, 0) + 1
        
        return sorted(growth_data.items())
    
    def export_detailed_report(self, filename: str = "detailed_report.json"):
        """Export a comprehensive report to JSON file."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "project_stats": self.get_project_stats(),
            "leaderboard": [c.to_dict() for c in self.get_leaderboard()],
            "repository_stats": dict(self.get_repository_leaderboard()),
            "daily_contributions": self.get_daily_contribution_stats(),
            "contributor_growth": dict(self.get_contributor_growth_over_time()),
            "completion_analysis": {
                "completed_count": len(self.get_completed_contributors()),
                "in_progress_count": len(self.get_all_contributors()) - len(self.get_completed_contributors()),
                "completion_percentage": len(self.get_completed_contributors()) / len(self.get_all_contributors()) * 100 if self.get_all_contributors() else 0
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Detailed report exported to {filename}")
        return report


def simulate_realistic_hacktoberfest_data(tracker: AdvancedProjectTracker):
    """Simulate realistic Hacktoberfest contribution data."""
    print("🎲 Simulating realistic Hacktoberfest data...")
    
    # Sample contributors with varied contribution patterns
    contributors_data = [
        ("Sarah Chen", "sarah_dev", "sarah@techcorp.com", 6),  # Overachiever
        ("Mike Rodriguez", "mike_codes", "mike@startup.io", 4),  # Exactly 4
        ("Emily Davis", "emily_py", "emily@university.edu", 3),  # Almost there
        ("Alex Thompson", "alex_js", "alex@freelance.com", 5),  # Overachiever
        ("Jordan Kim", "jordan_ml", "jordan@datacom.com", 2),  # Getting started
        ("Taylor Wilson", "taylor_web", "taylor@agency.com", 4),  # Exactly 4
        ("Casey Brown", "casey_ops", "casey@cloudtech.com", 1),  # Just started
        ("River Johnson", "river_security", "river@cybersec.com", 7),  # Very active
    ]
    
    # Sample repositories representing different project types
    repositories = [
        "web-dashboard", "api-backend", "mobile-app", "data-analytics", 
        "documentation-site", "automation-tools", "security-scanner", 
        "ml-pipeline", "frontend-components", "testing-framework"
    ]
    
    # Contribution types with weights (more common types have higher weights)
    contribution_types = [
        ("bug-fix", 0.3), ("feature", 0.25), ("documentation", 0.2), 
        ("refactoring", 0.1), ("testing", 0.1), ("performance", 0.05)
    ]
    
    # Add contributors and their contributions
    for name, username, email, target_contributions in contributors_data:
        contributor = tracker.add_contributor(name, username, email)
        
        # Simulate joining at different times during October
        import random
        join_day = random.randint(1, 15)  # Joined sometime in first half of October
        contributor.joined_date = datetime(2025, 10, join_day)
        
        # Add contributions with realistic timing
        for i in range(target_contributions):
            # Pick random repo and contribution type
            repo = random.choice(repositories)
            contrib_type = random.choices(
                [ct[0] for ct in contribution_types], 
                weights=[ct[1] for ct in contribution_types]
            )[0]
            
            # Generate realistic descriptions
            descriptions = {
                "bug-fix": [
                    "Fixed null pointer exception in user authentication",
                    "Resolved memory leak in data processing module",
                    "Fixed broken responsive design on mobile devices",
                    "Corrected timezone handling for international users",
                    "Fixed race condition in concurrent file operations"
                ],
                "feature": [
                    "Added user profile customization options",
                    "Implemented dark mode theme support",
                    "Added export functionality for data reports",
                    "Created automated backup system",
                    "Added real-time notification system"
                ],
                "documentation": [
                    "Updated API documentation with new endpoints",
                    "Added comprehensive setup guide for new contributors",
                    "Improved code comments and inline documentation",
                    "Created user manual with screenshots",
                    "Added troubleshooting guide for common issues"
                ],
                "refactoring": [
                    "Refactored authentication module for better maintainability",
                    "Simplified complex query logic in data layer",
                    "Extracted reusable components from monolithic code",
                    "Improved code organization and structure",
                    "Optimized database query performance"
                ],
                "testing": [
                    "Added comprehensive unit tests for user service",
                    "Implemented integration tests for API endpoints",
                    "Added end-to-end tests for critical user flows",
                    "Improved test coverage for edge cases",
                    "Added performance benchmarking tests"
                ],
                "performance": [
                    "Optimized database queries for faster response times",
                    "Implemented caching layer for frequently accessed data",
                    "Reduced bundle size by removing unused dependencies",
                    "Optimized image loading and compression",
                    "Improved memory usage in data processing"
                ]
            }
            
            description = random.choice(descriptions[contrib_type])
            pr_number = random.randint(100, 999)
            
            # Simulate contribution dates spread throughout October
            contrib_day = join_day + random.randint(0, 30 - join_day)
            contribution_date = datetime(2025, 10, min(contrib_day, 31))
            
            tracker.add_contribution(username, repo, contrib_type, description, pr_number)
            
            # Manually set the contribution date for realistic timing
            if tracker.get_contributor(username).contributions:
                tracker.get_contributor(username).contributions[-1]["date"] = contribution_date.isoformat()
    
    print(f"✅ Added {len(contributors_data)} contributors with realistic contribution patterns")


def main():
    """Main function demonstrating advanced features."""
    print("🚀 Hacktoberfest 2025 - Advanced Project Tracker Example 🚀\n")
    
    # Create advanced tracker
    tracker = AdvancedProjectTracker("Advanced Hacktoberfest Analytics")
    
    # Simulate realistic data
    simulate_realistic_hacktoberfest_data(tracker)
    
    # Display basic statistics
    print("\n" + "="*70)
    tracker.print_stats()
    
    # Show repository leaderboard
    print("\n" + "="*70)
    print("🏆 Repository Leaderboard (Most Active Repositories)")
    print("="*70)
    repo_leaderboard = tracker.get_repository_leaderboard()
    for i, (repo_name, stats) in enumerate(repo_leaderboard[:5], 1):
        print(f"{i:2d}. {repo_name}")
        print(f"    Contributions: {stats['contribution_count']}")
        print(f"    Contributors: {stats['unique_contributors']}")
        print(f"    Top Types: {', '.join(sorted(stats['types'].keys())[:3])}")
        print()
    
    # Show daily contribution trends
    print("="*70)
    print("📈 Daily Contribution Trends")
    print("="*70)
    daily_stats = tracker.get_daily_contribution_stats()
    for date, count in sorted(daily_stats.items())[-7:]:  # Last 7 days
        bar = "█" * min(count, 20)  # Visual bar chart
        print(f"{date}: {count:2d} contributions {bar}")
    
    # Show contributor growth
    print(f"\n📊 Contributor Growth Over Time:")
    growth_data = tracker.get_contributor_growth_over_time()
    cumulative = 0
    for date, new_contributors in growth_data:
        cumulative += new_contributors
        print(f"  {date}: +{new_contributors} (Total: {cumulative})")
    
    # Analyze contribution patterns
    print(f"\n🔍 Advanced Analysis:")
    
    # Find most prolific contributor
    leaderboard = tracker.get_leaderboard()
    if leaderboard:
        top_contributor = leaderboard[0]
        print(f"  🥇 Top Contributor: {top_contributor.name} ({top_contributor.get_contribution_count()} contributions)")
    
    # Find most popular repository
    if repo_leaderboard:
        top_repo = repo_leaderboard[0]
        print(f"  🏆 Most Active Repository: {top_repo[0]} ({top_repo[1]['contribution_count']} contributions)")
    
    # Contribution type distribution
    all_types = {}
    for contributor in tracker.get_all_contributors():
        for contrib in contributor.contributions:
            contrib_type = contrib["type"]
            all_types[contrib_type] = all_types.get(contrib_type, 0) + 1
    
    if all_types:
        most_common_type = max(all_types.items(), key=lambda x: x[1])
        print(f"  📝 Most Common Contribution Type: {most_common_type[0]} ({most_common_type[1]} occurrences)")
    
    # Export detailed report
    print(f"\n📋 Generating detailed analytics report...")
    report = tracker.export_detailed_report("hacktoberfest_analytics_report.json")
    
    # Custom analysis: Find contributors who might need encouragement
    in_progress = [c for c in tracker.get_all_contributors() if not c.is_hacktoberfest_complete()]
    if in_progress:
        print(f"\n🎯 Contributors who could use encouragement:")
        for contributor in sorted(in_progress, key=lambda c: c.get_contribution_count(), reverse=True):
            remaining = 4 - contributor.get_contribution_count()
            print(f"  • {contributor.name}: {contributor.get_contribution_count()}/4 ({remaining} more needed)")
    
    # Success summary
    completed = tracker.get_completed_contributors()
    print(f"\n🎉 Hacktoberfest 2025 Summary:")
    print(f"  Total Contributors: {len(tracker.get_all_contributors())}")
    print(f"  Completed Hacktoberfest: {len(completed)}")
    print(f"  Total Contributions: {sum(c.get_contribution_count() for c in tracker.get_all_contributors())}")
    print(f"  Success Rate: {(len(completed) / len(tracker.get_all_contributors()) * 100):.1f}%")
    
    print(f"\n✨ Advanced analysis complete! Check the generated report for more details.")


if __name__ == "__main__":
    main()