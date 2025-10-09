# 📚 API Documentation

This document provides detailed information about the Hacktoberfest 2025 Python Project Tracker API.

## 🏗️ Architecture Overview

The project is structured with two main classes:
- `Contributor`: Manages individual contributor information
- `ProjectTracker`: Manages the overall project and all contributors

## 📋 Contributor Class

### Constructor
```python
Contributor(name: str, github_username: str, email: str = "")
```

Creates a new contributor instance.

**Parameters:**
- `name` (str): Full name of the contributor
- `github_username` (str): GitHub username
- `email` (str, optional): Email address

**Example:**
```python
from hacktoberfest_app import Contributor

contributor = Contributor("Jane Doe", "janedoe", "jane@example.com")
```

### Methods

#### `add_contribution(repo_name, contribution_type, description, pr_number=None)`
Adds a new contribution to the contributor's record.

**Parameters:**
- `repo_name` (str): Name of the repository
- `contribution_type` (str): Type of contribution (e.g., 'bug-fix', 'feature', 'documentation')
- `description` (str): Description of the contribution
- `pr_number` (int, optional): Pull request number

**Example:**
```python
contributor.add_contribution(
    "awesome-project", 
    "bug-fix", 
    "Fixed authentication issue", 
    pr_number=42
)
```

#### `get_contribution_count() -> int`
Returns the total number of contributions.

#### `get_contributions_by_type(contribution_type) -> List[Dict]`
Returns all contributions of a specific type.

#### `is_hacktoberfest_complete() -> bool`
Checks if the contributor has completed Hacktoberfest (4+ contributions).

#### `to_dict() -> Dict`
Converts contributor to dictionary representation for serialization.

### Properties
- `name`: Full name
- `github_username`: GitHub username
- `email`: Email address
- `contributions`: List of contribution dictionaries
- `joined_date`: Date when contributor was added

## 🗂️ ProjectTracker Class

### Constructor
```python
ProjectTracker(project_name: str = "Hacktoberfest 2025", data_file: str = "contributors.json")
```

Creates a new project tracker instance.

**Parameters:**
- `project_name` (str): Name of the project
- `data_file` (str): File to store contributor data

**Example:**
```python
from hacktoberfest_app import ProjectTracker

tracker = ProjectTracker("My Awesome Project")
```

### Methods

#### `add_contributor(name, github_username, email="") -> Contributor`
Adds a new contributor to the project.

**Example:**
```python
contributor = tracker.add_contributor("John Doe", "johndoe", "john@example.com")
```

#### `get_contributor(github_username) -> Optional[Contributor]`
Retrieves a contributor by their GitHub username.

#### `add_contribution(github_username, repo_name, contribution_type, description, pr_number=None) -> bool`
Adds a contribution for a specific contributor.

**Example:**
```python
success = tracker.add_contribution(
    "johndoe", 
    "my-repo", 
    "feature", 
    "Added user authentication",
    pr_number=123
)
```

#### `get_all_contributors() -> List[Contributor]`
Returns a list of all contributors.

#### `get_completed_contributors() -> List[Contributor]`
Returns contributors who have completed Hacktoberfest.

#### `get_leaderboard() -> List[Contributor]`
Returns contributors sorted by number of contributions (descending).

#### `get_project_stats() -> Dict`
Returns overall project statistics.

**Example Response:**
```python
{
    "project_name": "Hacktoberfest 2025",
    "total_contributors": 15,
    "total_contributions": 67,
    "completed_hacktoberfest": 8,
    "completion_rate": "53.3%",
    "created_date": "2025-10-01T10:00:00"
}
```

#### `save_data()` and `load_data()`
Persist and load data from JSON file.

#### `print_leaderboard()` and `print_stats()`
Print formatted output to console.

## 🖥️ Command Line Interface

### Basic Commands

```bash
# Add contributor
python src/main.py --add-contributor "Name" "username" "email"

# Add contribution
python src/main.py --add-contribution "username" "repo" "type" "description" --pr 123

# View statistics
python src/main.py --stats

# Show leaderboard
python src/main.py --leaderboard

# List all contributors
python src/main.py --list-contributors

# Get contributor info
python src/main.py --contributor-info "username"

# Interactive mode
python src/main.py --interactive
```

### Interactive Mode Commands

In interactive mode, use these commands:
- `stats` - Show project statistics
- `leaderboard` - Show contributor leaderboard
- `list` - List all contributors
- `add contributor` - Add a new contributor (interactive)
- `add contribution` - Add a contribution (interactive)
- `info <username>` - Show detailed info for a contributor
- `help` - Show available commands
- `quit`/`exit` - Exit the program

## 📊 Data Structure

### Contributor Data Format
```json
{
  "name": "John Doe",
  "github_username": "johndoe",
  "email": "john@example.com",
  "joined_date": "2025-10-01T10:00:00",
  "contributions": [
    {
      "repo_name": "awesome-project",
      "type": "bug-fix",
      "description": "Fixed login issue",
      "pr_number": 42,
      "date": "2025-10-01T11:30:00"
    }
  ],
  "contribution_count": 1,
  "hacktoberfest_complete": false
}
```

### Project Data Format
```json
{
  "project_name": "Hacktoberfest 2025",
  "created_date": "2025-10-01T10:00:00",
  "contributors": {
    "johndoe": { /* contributor data */ },
    "janedoe": { /* contributor data */ }
  }
}
```

## 🔧 Configuration

### Environment Variables
- `HACKTOBERFEST_DATA_FILE`: Custom path for data file (default: "contributors.json")
- `HACKTOBERFEST_PROJECT_NAME`: Custom project name

### Example Configuration
```bash
export HACKTOBERFEST_DATA_FILE="/path/to/custom/data.json"
export HACKTOBERFEST_PROJECT_NAME="My Custom Project"
```

## 🧪 Testing Examples

### Unit Test Example
```python
import pytest
from hacktoberfest_app import Contributor, ProjectTracker

def test_contributor_creation():
    contributor = Contributor("Test User", "testuser", "test@example.com")
    assert contributor.name == "Test User"
    assert contributor.github_username == "testuser"
    assert contributor.get_contribution_count() == 0

def test_add_contribution():
    contributor = Contributor("Test User", "testuser")
    contributor.add_contribution("repo", "bug-fix", "Fixed bug", 123)
    assert contributor.get_contribution_count() == 1
    assert contributor.contributions[0]["pr_number"] == 123
```

## 🚀 Advanced Usage

### Custom Contribution Types
The system supports any contribution type string. Common types include:
- `bug-fix`: Bug fixes
- `feature`: New features
- `documentation`: Documentation improvements
- `refactoring`: Code refactoring
- `testing`: Test additions/improvements
- `performance`: Performance optimizations

### Extending the Classes
```python
from hacktoberfest_app import ProjectTracker

class CustomProjectTracker(ProjectTracker):
    def get_top_contributor(self):
        """Get the contributor with the most contributions."""
        leaderboard = self.get_leaderboard()
        return leaderboard[0] if leaderboard else None
    
    def get_contributions_by_repo(self, repo_name):
        """Get all contributions for a specific repository."""
        all_contributions = []
        for contributor in self.get_all_contributors():
            for contrib in contributor.contributions:
                if contrib["repo_name"] == repo_name:
                    all_contributions.append({
                        "contributor": contributor.name,
                        **contrib
                    })
        return all_contributions
```

## 🔍 Error Handling

The API includes proper error handling:
- Invalid contributor usernames return `None` or `False`
- File I/O errors are caught and logged
- JSON parsing errors are handled gracefully
- Type validation on inputs

## 📈 Performance Considerations

- Data is loaded once at startup and cached in memory
- JSON serialization happens only on data changes
- Large datasets (1000+ contributors) should consider database backend
- File-based storage is suitable for small to medium projects

For more examples and advanced usage, see the `examples/` directory in the project.