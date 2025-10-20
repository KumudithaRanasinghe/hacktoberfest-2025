# 📊 CSV Export/Import Feature Documentation

## Overview

The Hacktoberfest 2025 Project Tracker includes comprehensive CSV import/export functionality for managing data in spreadsheet format. This allows you to:

- **Export** contributor data, contributions, and metrics to CSV files
- **Import** data from CSV files to populate the tracker
- **Backup** data in human-readable format
- **Share** data with team members
- **Integrate** with other tools and spreadsheet applications

## Features

### Export Capabilities

✅ **Export Contributors**
- Name, GitHub username, email
- Join date, contribution count
- Hacktoberfest completion status

✅ **Export Contributions**
- Contributor information
- Repository name and PR details
- Contribution type and description
- Contribution date

✅ **Export Metrics**
- Engagement scores
- Contribution analysis
- Days active and streaks
- Contribution types and repositories

✅ **Batch Export**
- Export all data at once
- Timestamped filenames
- Organized directory structure

### Import Capabilities

✅ **Import Contributors**
- Add multiple contributors from CSV
- Preserve joined dates
- Validate data

✅ **Import Contributions**
- Link contributions to existing contributors
- Restore PR numbers and dates
- Validate repository and type information

✅ **CSV Templates**
- Generate template files
- Pre-formatted headers
- Example data included

## CLI Commands

### Generate CSV Template

Generate a template file to fill with data:

```bash
# Generate contributors template
python src/main.py --csv-template contributors --csv-template-file contributors_template.csv

# Generate contributions template
python src/main.py --csv-template contributions --csv-template-file contributions_template.csv
```

Output files are ready to edit in Excel, Google Sheets, or any text editor.

### Export Data to CSV

Export all project data to CSV files:

```bash
# Export only contributors
python src/main.py --export-csv contributors --export-csv-path contributors.csv

# Export only contributions
python src/main.py --export-csv contributions --export-csv-path contributions.csv

# Export only metrics
python src/main.py --export-csv metrics --export-csv-path metrics.csv

# Export all data (creates timestamped files in exports/ directory)
python src/main.py --export-csv all
```

**Output Structure:**
```
exports/
├── contributors_20251019_153000.csv
├── contributions_20251019_153000.csv
└── metrics_20251019_153000.csv
```

### Import Data from CSV

Import contributors and contributions from CSV files:

```bash
# Import only contributors
python src/main.py --import-contributors contributors.csv

# Import contributors and contributions
python src/main.py --import-contributors contributors.csv --import-contributions contributions.csv
```

## CSV File Formats

### Contributors CSV Format

**File:** `contributors.csv`

```csv
name,github_username,email,joined_date,contribution_count,hacktoberfest_complete
John Doe,johndoe,john@example.com,2025-10-01,4,Yes
Jane Smith,janesmith,jane@example.com,2025-10-02,3,No
```

**Columns:**
- `name` - Full name (required)
- `github_username` - GitHub handle (required)
- `email` - Email address (optional)
- `joined_date` - ISO format date YYYY-MM-DD HH:MM:SS (optional)
- `contribution_count` - Number of contributions (read-only, for reference)
- `hacktoberfest_complete` - "Yes" or "No" (read-only, for reference)

### Contributions CSV Format

**File:** `contributions.csv`

```csv
github_username,contributor_name,repo_name,contribution_type,description,pr_number,date
johndoe,John Doe,my-repo,bug-fix,Fixed login issue,123,2025-10-05T10:30:00
janesmith,Jane Smith,other-repo,feature,Added new feature,124,2025-10-06T14:20:00
```

**Columns:**
- `github_username` - GitHub handle (required, must exist in contributors)
- `contributor_name` - Full name (for reference)
- `repo_name` - Repository name (required)
- `contribution_type` - Type: "bug-fix", "feature", "documentation", etc. (required)
- `description` - Description of contribution (required)
- `pr_number` - Pull request number (optional)
- `date` - ISO format date YYYY-MM-DD (optional)

### Metrics CSV Format

**File:** `metrics.csv`

```csv
github_username,contributor_name,total_contributions,joined_date,days_active,hacktoberfest_complete,contribution_types,repositories,engagement_score
johndoe,John Doe,4,2025-10-01,18,Yes,bug-fix:2; feature:2,my-repo:3; other-repo:1,87.50
```

**Columns:**
- `github_username` - GitHub handle
- `contributor_name` - Full name
- `total_contributions` - Contribution count
- `joined_date` - Join date
- `days_active` - Days since joining
- `hacktoberfest_complete` - "Yes" or "No"
- `contribution_types` - Semicolon-separated type:count pairs
- `repositories` - Semicolon-separated repo:count pairs
- `engagement_score` - Engagement score (0-100)

## Python API

### Using CSV Functions in Code

```python
from Contribute_Checker import ProjectTracker

tracker = ProjectTracker()

# Export data
tracker.export_to_csv("contributors", "contributors.csv")
tracker.export_to_csv("contributions", "contributions.csv")
tracker.export_to_csv("metrics", "metrics.csv")
tracker.export_to_csv("all", "exports/")

# Import data
tracker.import_from_csv("contributors.csv", "contributions.csv")

# Generate templates
tracker.save_csv_template("contributors", "template_contributors.csv")
tracker.save_csv_template("contributions", "template_contributions.csv")

# Get template as string
template = tracker.get_csv_template("contributors")
print(template)
```

### Using CSVHandler Directly

```python
from Contribute_Checker.csv_handler import CSVHandler
from Contribute_Checker import ProjectTracker

tracker = ProjectTracker()
contributors = tracker.get_all_contributors()

# Export functions
CSVHandler.export_contributors_to_csv(contributors, "contributors.csv")
CSVHandler.export_contributions_to_csv(contributors, "contributions.csv")
CSVHandler.export_metrics_to_csv(contributors, "metrics.csv")
CSVHandler.export_all_to_csv(contributors, "exports/")

# Import functions
imported_contributors, errors = CSVHandler.import_contributors_from_csv("contributors.csv")

# Templates
CSVHandler.save_csv_template("contributors", "template.csv")
template_content = CSVHandler.get_csv_template("contributors")
```

## Usage Examples

### Example 1: Export Project Data

```bash
# Export everything
python src/main.py --export-csv all

# View the exports
ls -la exports/
```

Output:
```
contributors_20251019_153000.csv
contributions_20251019_153000.csv
metrics_20251019_153000.csv
```

### Example 2: Create and Edit Template

```bash
# Generate template
python src/main.py --csv-template contributors --csv-template-file my_contributors.csv

# Edit in Excel/Google Sheets
# ... add your data ...

# Import the data
python src/main.py --import-contributors my_contributors.csv
```

### Example 3: Backup and Restore

```bash
# Backup current data
python src/main.py --export-csv all --export-csv-path backups/

# Later, restore from backup
cp backups/contributors_*.csv contributors.csv
cp backups/contributions_*.csv contributions.csv
python src/main.py --import-contributors contributors.csv --import-contributions contributions.csv
```

### Example 4: Migrate Data Between Systems

```bash
# System A: Export data
python src/main.py --export-csv all

# Copy files to System B
scp exports/* user@system-b:/tmp/

# System B: Import data
python src/main.py --import-contributors /tmp/contributors_*.csv --import-contributions /tmp/contributions_*.csv
```

## Data Format Details

### Date Format

All dates should be in ISO 8601 format:
- **Date only:** `2025-10-19`
- **Date and time:** `2025-10-19T15:30:00`
- **With timezone:** `2025-10-19T15:30:00+00:00`

### GitHub Username Format

- Use lowercase only
- No @ symbol at the beginning
- No spaces or special characters

Example valid usernames:
- `john_doe` ✅
- `janedoe1` ✅
- `john-smith` ✅
- `@johndoe` ❌
- `John Doe` ❌

### Contribution Types

Standard contribution types:
- `bug-fix`
- `feature`
- `documentation`
- `test`
- `refactor`
- `performance`
- `security`
- Other custom types are supported

### Email Format

Valid email addresses:
- `user@example.com` ✅
- `john.doe@company.co.uk` ✅
- `invalid@email` ❌
- `missing@` ❌

## Troubleshooting

### Import Fails with Encoding Error

**Problem:** "UnicodeDecodeError"

**Solution:**
- Ensure CSV file is saved as UTF-8 encoding
- In Excel: File → Save As → CSV UTF-8
- In Google Sheets: Download as CSV (automatically UTF-8)

### Contributors Not Found During Contribution Import

**Problem:** "Contributor {username} not found"

**Solution:**
- Ensure contributors CSV is imported first
- Verify GitHub usernames match exactly (case-sensitive)
- Check for typos or extra spaces

### CSV File Not Created/Found

**Problem:** "File not found" or file not created

**Solution:**
- Check write permissions in output directory
- Ensure directory exists for the output path
- Use absolute paths for clarity: `/full/path/to/file.csv`

### Date Format Issues

**Problem:** "Invalid date format"

**Solution:**
- Use ISO 8601 format: `2025-10-19` or `2025-10-19T15:30:00`
- Don't use locale-specific formats (e.g., `10/19/2025`)
- Remove timezone if not needed

## Advanced Usage

### Automated Daily Backups

Create a backup script:

```python
import os
import subprocess
from datetime import datetime

def backup_data():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/{timestamp}"
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Run export
    subprocess.run([
        "python", "src/main.py",
        "--export-csv", "all",
        "--export-csv-path", backup_dir
    ])
    
    print(f"Backup created: {backup_dir}")

if __name__ == "__main__":
    backup_data()
```

Run daily with cron (Linux/Mac):
```bash
0 2 * * * cd /path/to/project && python backup.py
```

Or Windows Task Scheduler:
```
schtasks /create /tn "Hacktoberfest Backup" /tr "python backup.py" /sc daily /st 02:00
```

### Data Validation

Validate CSV before import:

```python
import csv

def validate_csv(filename):
    errors = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            if not row.get('github_username'):
                errors.append(f"Row {row_num}: Missing GitHub username")
            if not row.get('name'):
                errors.append(f"Row {row_num}: Missing name")
    
    return errors

errors = validate_csv("contributors.csv")
if errors:
    print("Validation errors:")
    for error in errors:
        print(f"  • {error}")
else:
    print("✅ CSV validation passed")
```

### Merge Multiple CSVs

Combine data from multiple sources:

```python
from Contribute_Checker import ProjectTracker
import csv

tracker = ProjectTracker()

# Import from multiple CSV files
csv_files = ["contributors_team_a.csv", "contributors_team_b.csv"]

for csv_file in csv_files:
    print(f"Importing {csv_file}...")
    tracker.import_from_csv(csv_file)

# Export merged data
tracker.export_to_csv("all", "merged/")
```

## Integration with Other Tools

### Google Sheets Integration

1. Export CSV from tracker:
   ```bash
   python src/main.py --export-csv contributors --export-csv-path contributors.csv
   ```

2. Upload to Google Sheets:
   - Go to Google Sheets
   - File → Open → Upload
   - Select the CSV file
   - Edit in Google Sheets
   - Download as CSV
   - Import back into tracker

### Excel Integration

1. Export CSV from tracker
2. Open in Excel
3. Edit and save (ensure UTF-8 encoding)
4. Save as CSV
5. Import back into tracker

### Database Integration

Export to SQL:
```python
import sqlite3
import csv

tracker = ProjectTracker()
tracker.export_to_csv("contributors", "contributors.csv")

# Create SQLite database
conn = sqlite3.connect('hacktoberfest.db')
cursor = conn.cursor()

with open('contributors.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO contributors (name, github_username, email, joined_date)
            VALUES (?, ?, ?, ?)
        ''', (row['name'], row['github_username'], row['email'], row['joined_date']))

conn.commit()
```

## Performance Considerations

- **Large Files:** CSV import/export with 1000+ contributors may take several seconds
- **Memory:** All data is loaded into memory; not suitable for extremely large datasets
- **UTF-8:** Always use UTF-8 encoding for international characters

## Best Practices

1. **Regular Backups:** Export data weekly
2. **Version Control:** Keep backup CSVs in version control (without sensitive data)
3. **Validation:** Always validate CSV before importing
4. **Documentation:** Document custom contribution types in your CSV
5. **Encoding:** Always use UTF-8 encoding
6. **Timestamps:** Use ISO 8601 format for dates

## Support

For issues or questions:
- Check main `README.md`
- Review examples in this documentation
- Open an issue on GitHub

---

Happy data management! 📊✨
