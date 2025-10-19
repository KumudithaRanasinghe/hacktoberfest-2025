#!/usr/bin/env python3
"""Test script for Performance Metrics feature."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Contribute_Checker import ProjectTracker

# Create tracker
tracker = ProjectTracker(data_file='test_metrics.json')

# Add test contributors
alice = tracker.add_contributor('Alice Johnson', 'alice', 'alice@example.com')
bob = tracker.add_contributor('Bob Smith', 'bob', 'bob@example.com')
carol = tracker.add_contributor('Carol White', 'carol', 'carol@example.com')

# Add contributions
for i in range(5):
    tracker.add_contribution('alice', 'repo-a', 'bug-fix' if i % 2 == 0 else 'feature', f'Fix {i}', i+100)

for i in range(4):
    tracker.add_contribution('bob', 'repo-b', 'documentation', f'Doc {i}', i+200)

for i in range(2):
    tracker.add_contribution('carol', 'repo-c', 'feature', f'Feature {i}', i+300)

# Get metrics
metrics = tracker.get_project_performance_metrics()
print('📊 Project Metrics Test Results:')
print(f'  Total Contributors: {metrics["total_contributors"]}')
print(f'  Total Contributions: {metrics["total_contributions"]}')
print(f'  Completion Rate: {metrics["hacktoberfest_completion_rate"]:.1f}%')
print(f'  Average per Contributor: {metrics["average_contributions_per_contributor"]:.2f}')

rankings = tracker.get_contributors_ranking()
print('\n🏆 Engagement Rankings:')
for rank in rankings[:3]:
    print(f'  {rank["rank"]}. {rank["name"]} - Score: {rank["engagement_score"]:.1f}')

# Get individual metrics
alice_metrics = tracker.get_contributor_metrics('alice')
print(f'\n👤 Alice Metrics:')
print(f'  Total Contributions: {alice_metrics["total_contributions"]}')
print(f'  Engagement Score: {tracker.get_engagement_score("alice"):.1f}/100')
print(f'  Hacktoberfest Complete: {"✅ Yes" if alice_metrics["hacktoberfest_complete"] else "❌ No"}')

# Get insights
insights = tracker.get_performance_insights()
print('\n💡 Performance Insights:')
for highlight in insights['highlights']:
    print(f'  {highlight}')

print('\n✅ Performance Metrics Test Completed Successfully!')
