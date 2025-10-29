# Search & Filter Documentation

## Overview

The Search & Filter feature provides comprehensive capabilities for finding and filtering contributors and contributions in the Hacktoberfest 2025 Project Tracker.

## Features

### 1. **Contributor Search**
   - Search by name, username, or email
   - Multiple search types: exact, contains, starts_with, ends_with, regex, fuzzy
   - Case-sensitive and case-insensitive options
   - Search in specific fields or all fields

### 2. **Contribution Search**
   - Search across contribution descriptions, repository names, and types
   - Flexible search options with multiple search types
   - Find contributions by keyword across all fields

### 3. **Advanced Filtering**
   - Filter contributors by:
     - Contribution count (min/max)
     - Hacktoberfest completion status
     - Email availability
     - Join date range
     - Contribution type

   - Filter contributions by:
     - Type (bug-fix, feature, documentation, etc.)
     - Repository name
     - Date range
     - PR availability
     - Specific contributor

### 4. **Sorting**
   - Sort by: name, username, contributions, joined_date
   - Sort order: ascending or descending

### 5. **Statistics**
   - Get overview of searchable data
   - Contribution types distribution
   - Repository breakdown
   - Completion rate analysis

## CLI Usage

### Basic Contributor Search

```bash
# Search for contributor by name or username
python main.py --search-contributors "john"

# Case-sensitive search
python main.py --search-contributors "John" --case-sensitive

# Search only in email field
python main.py --search-contributors "gmail" --search-field "email"

# Search in username only
python main.py --search-contributors "doe" --search-field "username"
```

### Advanced Search Types

```bash
# Exact match
python main.py --search-contributors "john_doe" --search-type exact

# Starts with
python main.py --search-contributors "john" --search-type starts_with

# Ends with
python main.py --search-contributors "doe" --search-type ends_with

# Regular expression
python main.py --search-contributors "john.*doe" --search-type regex --case-sensitive

# Fuzzy matching (characters in order, case-insensitive)
python main.py --search-contributors "jhndoe" --search-type fuzzy
```

### Contribution Search

```bash
# Search contributions by any field
python main.py --search-contributions "bug"

# Search in description only
python main.py --search-contributions "login issue" --search-in description

# Search by repository name
python main.py --search-contributions "my-repo" --search-in repo

# Search by contribution type
python main.py --search-contributions "feature" --search-in type

# Case-sensitive search
python main.py --search-contributions "Bug-Fix" --case-sensitive
```

### Contributor Filtering

```bash
# Filter by contribution count
python main.py --filter-contributors "min_contrib:5,max_contrib:20"

# Only completed contributors
python main.py --filter-contributors "completed_only:true"

# Only with email
python main.py --filter-contributors "has_email:true"

# Combine multiple filters
python main.py --filter-contributors "min_contrib:3,completed_only:true,has_email:true"
```

### Contribution Filtering

```bash
# Filter by type
python main.py --filter-contributions "type:bug-fix"

# Filter by repository
python main.py --filter-contributions "repo:my-awesome-repo"

# Only contributions with PRs
python main.py --filter-contributions "has_pr:true"

# Combine filters
python main.py --filter-contributions "repo:my-repo,type:feature,has_pr:true"
```

### Sorting Results

```bash
# Search and sort by name (ascending)
python main.py --search-contributors "john" --sort-by name --sort-order asc

# Sort by contribution count (descending)
python main.py --search-contributors "john" --sort-by contributions --sort-order desc

# Sort by joined date (oldest first)
python main.py --search-contributors "john" --sort-by joined_date --sort-order asc

# Sort by username (newest registrations)
python main.py --search-contributors "john" --sort-by username --sort-order desc
```

### Statistics

```bash
# Get search and filter statistics
python main.py --search-stats

# Output includes:
# - Total contributors
# - Total contributions
# - Contributors with email
# - Completed Hacktoberfest contributors
# - Contribution types breakdown
# - Repository breakdown
```

## Python API Usage

### Basic Usage

```python
from Contribute_Checker import ProjectTracker, SearchType, SortOrder

# Initialize tracker
tracker = ProjectTracker()

# Search contributors
results = tracker.search_contributors(
    query="john",
    search_type=SearchType.CONTAINS,
    search_field="name"
)

# Search contributions
contrib_results = tracker.search_contributions(
    query="bug fix",
    search_in="description"
)

# Filter contributors
filtered = tracker.filter_contributors(
    min_contributions=5,
    max_contributions=20,
    completed_only=True
)

# Filter contributions
filtered_contribs = tracker.filter_contributions(
    contribution_type="bug-fix",
    repo_name="my-repo"
)
```

### Advanced Search with Filters

```python
# Complex filter dictionary
filters = {
    "query": "john",
    "search_field": "all",
    "search_type": "contains",
    "min_contributions": 3,
    "max_contributions": 50,
    "completed_only": False,
    "has_email": True
}

results = tracker.advanced_search(
    filters=filters,
    sort_by="contributions",
    sort_order=SortOrder.DESCENDING
)

# Get quick statistics
stats = tracker.get_quick_search_stats(results)
print(f"Found {stats['result_count']} contributors")
print(f"Total contributions: {stats['total_contributions']}")
print(f"Average: {stats['average_contributions']:.1f}")
```

### Sorting

```python
# Sort contributors
sorted_contrib = tracker.sort_contributors(
    sort_by="contributions",
    order=SortOrder.DESCENDING
)

# Sort with specific list
all_contributors = tracker.get_all_contributors()
sorted_list = tracker.sort_contributors(
    contributors=all_contributors,
    sort_by="joined_date",
    order=SortOrder.ASCENDING
)
```

### Using SearchEngine Directly

```python
from Contribute_Checker import SearchEngine, SearchType

engine = SearchEngine()

# Get statistics
stats = engine.get_statistics(contributors_list)
print(f"Total contributions by type: {stats['contribution_types']}")
print(f"Total repositories: {len(stats['repositories'])}")

# Fuzzy matching
results = engine.search_contributors(
    contributors_list,
    query="jdoe",
    search_type=SearchType.FUZZY
)

# Regex search
import re
results = engine.search_contributors(
    contributors_list,
    query=r"john.*doe",
    search_type=SearchType.REGEX,
    case_sensitive=False
)
```

## Search Types Explained

### 1. **EXACT**
Matches the entire field value exactly.
- Query: "john"
- Matches: "john"
- Does NOT match: "john doe", "johnny", "John"

### 2. **CONTAINS** (Default)
Matches if query appears anywhere in the field.
- Query: "john"
- Matches: "john", "john doe", "johnny", "John"
- Does NOT match: "jon", "juan"

### 3. **STARTS_WITH**
Matches if field starts with the query.
- Query: "john"
- Matches: "john", "john doe", "johnny"
- Does NOT match: "the john", "JOHN"

### 4. **ENDS_WITH**
Matches if field ends with the query.
- Query: "john"
- Matches: "john", "mr john"
- Does NOT match: "johnny", "JOHN"

### 5. **REGEX**
Matches using regular expression patterns.
- Query: `john.*doe`
- Matches: "john doe", "john david doe", "john@doe"
- Query: `^j.*n$` (starts with 'j', ends with 'n')
- Matches: "john", "jane", "jon"

### 6. **FUZZY**
Matches if all query characters appear in order in the field (case-insensitive).
- Query: "jhndoe"
- Matches: "john doe", "john david doe", "johndoe"
- Does NOT match: "doe john"

## Filter Criteria Format

### Contributor Filters (Python API)

```python
# All optional parameters
tracker.filter_contributors(
    min_contributions=5,           # int
    max_contributions=20,          # int
    completed_only=True,           # bool
    has_email=True,               # bool
    joined_after=datetime(...),   # datetime
    joined_before=datetime(...),  # datetime
    contribution_type="bug-fix"   # str
)
```

### Contribution Filters (Python API)

```python
# All optional parameters
tracker.filter_contributions(
    contribution_type="feature",   # str
    repo_name="my-repo",          # str
    after_date=datetime(...),     # datetime
    before_date=datetime(...),    # datetime
    has_pr=True,                  # bool
    contributor_username="jdoe"   # str
)
```

## Quick Stats for Results

The `get_quick_search_stats()` method returns:

```python
{
    "result_count": 5,           # Number of results
    "total_contributions": 42,   # Sum of contributions
    "completed_count": 3,        # Completed Hacktoberfest
    "average_contributions": 8.4, # Mean contributions
    "completion_rate": 60.0      # Percentage
}
```

## Examples

### Find All Contributors Without Email

```bash
python main.py --search-contributors "" --filter-contributors "has_email:false"
```

### Find Bug-Fix Contributors Over 10 Contributions

```bash
python main.py --filter-contributors "min_contrib:10" --filter-contributions "type:bug-fix"
```

### Top Contributors by Contribution Count

```bash
python main.py --search-contributors "" --sort-by contributions --sort-order desc
```

### Recent Completed Contributors

```bash
python main.py --search-contributors "" --filter-contributors "completed_only:true" --sort-by joined_date --sort-order desc
```

### Search for Documentation Contributors

```bash
python main.py --filter-contributions "type:documentation"
```

### Find Contributors with Specific Email Domain

```bash
python main.py --search-contributors "@company.com" --search-field email --search-type contains
```

## Performance Notes

- **Search Performance**: Fast for small datasets (<10,000 contributors)
- **Regex Performance**: Slower than other search types; use sparingly
- **Fuzzy Search**: O(n*m) where n=text length, m=query length
- **Large Datasets**: Consider filtering before searching

## Limitations

- Email password not used in searches (privacy)
- Date range filters use ISO format: "2024-01-01"
- Regex patterns must be valid Python regex
- Case sensitivity only applies to text; booleans/numbers always exact match

## Error Handling

Invalid regex patterns will return no matches (fail gracefully).
Invalid filter criteria will raise a ValueError with helpful message.

```python
try:
    results = tracker.search_contributions(
        query="[invalid",  # Invalid regex
        search_type=SearchType.REGEX
    )
except re.error as e:
    print(f"Invalid regex: {e}")
```

## Best Practices

1. **Start Broad**: Search for general terms, then filter
2. **Use Case-Insensitive**: Default behavior catches variations
3. **Combine Filters**: Use multiple criteria for precise results
4. **Sort for Priority**: Use sort to organize large result sets
5. **Validate Input**: Escape special characters for regex searches

## Related Features

- **CSV Export**: Export search results to CSV
- **Performance Metrics**: Analyze contributor activity
- **Notifications**: Send targeted emails to search results
- **Email Notifications**: Notify specific contributor groups

## Troubleshooting

### No Results Found
- Try a broader search term
- Check case sensitivity setting
- Use CONTAINS instead of EXACT
- Try FUZZY for typos

### Too Many Results
- Add more specific filters
- Reduce search term length
- Use EXACT instead of CONTAINS
- Add min/max contribution filters

### Performance Issues
- Limit search scope with filters first
- Avoid complex regex patterns
- Consider exporting to CSV for offline analysis

## See Also

- [Project Tracker Documentation](../docs/API.md)
- [Email Notifications](EMAIL_NOTIFICATIONS.md)
- [Performance Metrics](PERFORMANCE_METRICS.md)
- [CSV Import/Export](CSV_IMPORT_EXPORT.md)
