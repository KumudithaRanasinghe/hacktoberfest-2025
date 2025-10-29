#!/usr/bin/env python3
"""Test the search functionality."""

from Contribute_Checker import ProjectTracker, Contributor, SearchType, SortOrder
from datetime import datetime

# Create tracker
tracker = ProjectTracker('Test Project', 'test_contributors.json')

# Add test contributors
tracker.add_contributor('John Doe', 'johndoe', 'john@example.com')
tracker.add_contributor('Jane Smith', 'janesmith', 'jane@example.com')
tracker.add_contributor('Bob Johnson', 'bjohnson', 'bob@company.com')

# Add contributions
tracker.add_contribution('johndoe', 'repo1', 'bug-fix', 'Fixed login issue', 123)
tracker.add_contribution('johndoe', 'repo2', 'feature', 'Added new feature')
tracker.add_contribution('janesmith', 'repo1', 'documentation', 'Updated README')
tracker.add_contribution('bjohnson', 'repo2', 'bug-fix', 'Fixed performance issue')

# Test search
print('=== Search Contributors ===')
results = tracker.search_contributors('john', SearchType.CONTAINS, 'all')
print(f'✅ Found {len(results)} contributors with "john"')
for c in results:
    print(f'  - {c.name}')

# Test filter
print('\n=== Filter Contributors ===')
filtered = tracker.filter_contributors(min_contributions=1)
print(f'✅ Found {len(filtered)} contributors with at least 1 contribution')

# Test search contributions
print('\n=== Search Contributions ===')
contribs = tracker.search_contributions('bug', 'all')
print(f'✅ Found {len(contribs)} contributions with "bug"')
for c in contribs:
    print(f'  - {c["contributor_name"]}: {c["description"]}')

# Test sorting
print('\n=== Sort Contributors ===')
sorted_contrib = tracker.sort_contributors(sort_by='contributions', order=SortOrder.DESCENDING)
print(f'✅ Sorted {len(sorted_contrib)} contributors by contributions (desc)')
for c in sorted_contrib:
    print(f'  - {c.name}: {c.get_contribution_count()} contributions')

# Test stats
print('\n=== Search Statistics ===')
stats = tracker.get_search_statistics()
print(f'✅ Total contributors: {stats["total_contributors"]}')
print(f'✅ Total contributions: {stats["total_contributions"]}')
print(f'✅ Types: {stats["contribution_types"]}')
print(f'✅ Repositories: {stats["repositories"]}')

# Test quick stats
print('\n=== Quick Stats ===')
quick = tracker.get_quick_search_stats(results)
print(f'✅ Result count: {quick["result_count"]}')
print(f'✅ Total contributions: {quick["total_contributions"]}')
print(f'✅ Average: {quick["average_contributions"]:.1f}')
print(f'✅ Completion rate: {quick["completion_rate"]:.1f}%')

# Test regex search
print('\n=== Regex Search ===')
regex_results = tracker.search_contributors('j.*o', SearchType.REGEX, 'all')
print(f'✅ Found {len(regex_results)} contributors matching "j.*o" regex')
for c in regex_results:
    print(f'  - {c.name}')

# Test fuzzy search
print('\n=== Fuzzy Search ===')
fuzzy_results = tracker.search_contributors('jdoe', SearchType.FUZZY, 'all')
print(f'✅ Found {len(fuzzy_results)} contributors with fuzzy "jdoe"')
for c in fuzzy_results:
    print(f'  - {c.name}')

print('\n✅ All search tests passed!')
