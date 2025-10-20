"""
CSV Import/Export Module for Hacktoberfest 2025 Project Tracker.
Handles data serialization and deserialization to/from CSV format.
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from .contributor import Contributor


class CSVHandler:
    """Handles CSV export and import operations for project data."""
    
    # CSV column headers
    CONTRIBUTORS_HEADER = [
        "name",
        "github_username",
        "email",
        "joined_date",
        "contribution_count",
        "hacktoberfest_complete"
    ]
    
    CONTRIBUTIONS_HEADER = [
        "github_username",
        "contributor_name",
        "repo_name",
        "contribution_type",
        "description",
        "pr_number",
        "date"
    ]
    
    METRICS_HEADER = [
        "github_username",
        "contributor_name",
        "total_contributions",
        "joined_date",
        "days_active",
        "hacktoberfest_complete",
        "contribution_types",
        "repositories",
        "engagement_score"
    ]
    
    @staticmethod
    def export_contributors_to_csv(contributors: List[Contributor], 
                                   filename: str = "contributors.csv") -> bool:
        """
        Export contributors to CSV file.
        
        Args:
            contributors (List[Contributor]): List of contributors to export
            filename (str): Output CSV filename
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=CSVHandler.CONTRIBUTORS_HEADER)
                writer.writeheader()
                
                for contributor in contributors:
                    row = {
                        "name": contributor.name,
                        "github_username": contributor.github_username,
                        "email": contributor.email,
                        "joined_date": contributor.joined_date.isoformat(),
                        "contribution_count": contributor.get_contribution_count(),
                        "hacktoberfest_complete": "Yes" if contributor.is_hacktoberfest_complete() else "No"
                    }
                    writer.writerow(row)
            
            print(f"✅ Exported {len(contributors)} contributors to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting contributors to CSV: {e}")
            return False
    
    @staticmethod
    def export_contributions_to_csv(contributors: List[Contributor],
                                   filename: str = "contributions.csv") -> bool:
        """
        Export all contributions to CSV file.
        
        Args:
            contributors (List[Contributor]): List of contributors
            filename (str): Output CSV filename
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            total_contributions = 0
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=CSVHandler.CONTRIBUTIONS_HEADER)
                writer.writeheader()
                
                for contributor in contributors:
                    for contrib in contributor.contributions:
                        row = {
                            "github_username": contributor.github_username,
                            "contributor_name": contributor.name,
                            "repo_name": contrib.get("repo_name", ""),
                            "contribution_type": contrib.get("type", ""),
                            "description": contrib.get("description", ""),
                            "pr_number": contrib.get("pr_number", ""),
                            "date": contrib.get("date", "")
                        }
                        writer.writerow(row)
                        total_contributions += 1
            
            print(f"✅ Exported {total_contributions} contributions to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting contributions to CSV: {e}")
            return False
    
    @staticmethod
    def export_metrics_to_csv(contributors: List[Contributor],
                            filename: str = "metrics.csv") -> bool:
        """
        Export performance metrics to CSV file.
        
        Args:
            contributors (List[Contributor]): List of contributors
            filename (str): Output CSV filename
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            from .performance_metrics import PerformanceMetrics
            
            metrics_analyzer = PerformanceMetrics()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=CSVHandler.METRICS_HEADER)
                writer.writeheader()
                
                for contributor in contributors:
                    metrics = metrics_analyzer.calculate_contributor_metrics(contributor)
                    engagement = metrics_analyzer.get_engagement_score(contributor)
                    
                    # Format contribution types
                    types_str = "; ".join(
                        f"{k}:{v}" for k, v in metrics.get("contributions_by_type", {}).items()
                    ) if metrics.get("contributions_by_type") else ""
                    
                    # Format repositories
                    repos_str = "; ".join(
                        f"{k}:{v}" for k, v in metrics.get("contributions_by_repo", {}).items()
                    ) if metrics.get("contributions_by_repo") else ""
                    
                    row = {
                        "github_username": contributor.github_username,
                        "contributor_name": contributor.name,
                        "total_contributions": contributor.get_contribution_count(),
                        "joined_date": contributor.joined_date.isoformat(),
                        "days_active": metrics.get("days_active", 0),
                        "hacktoberfest_complete": "Yes" if contributor.is_hacktoberfest_complete() else "No",
                        "contribution_types": types_str,
                        "repositories": repos_str,
                        "engagement_score": f"{engagement:.2f}"
                    }
                    writer.writerow(row)
            
            print(f"✅ Exported metrics for {len(contributors)} contributors to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting metrics to CSV: {e}")
            return False
    
    @staticmethod
    def export_all_to_csv(contributors: List[Contributor],
                         output_dir: str = "exports") -> bool:
        """
        Export all data (contributors, contributions, metrics) to CSV files.
        
        Args:
            contributors (List[Contributor]): List of contributors
            output_dir (str): Output directory for CSV files
            
        Returns:
            bool: True if all exports successful, False otherwise
        """
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        success = True
        
        # Export contributors
        contributors_file = os.path.join(output_dir, f"contributors_{timestamp}.csv")
        success &= CSVHandler.export_contributors_to_csv(contributors, contributors_file)
        
        # Export contributions
        contributions_file = os.path.join(output_dir, f"contributions_{timestamp}.csv")
        success &= CSVHandler.export_contributions_to_csv(contributors, contributions_file)
        
        # Export metrics
        metrics_file = os.path.join(output_dir, f"metrics_{timestamp}.csv")
        success &= CSVHandler.export_metrics_to_csv(contributors, metrics_file)
        
        if success:
            print(f"\n✅ All data exported to {output_dir}/")
        
        return success
    
    @staticmethod
    def import_contributors_from_csv(filename: str) -> Tuple[List[Contributor], List[str]]:
        """
        Import contributors from CSV file.
        
        Args:
            filename (str): Input CSV filename
            
        Returns:
            Tuple[List[Contributor], List[str]]: (contributors, errors)
        """
        contributors = []
        errors = []
        
        try:
            if not os.path.exists(filename):
                errors.append(f"File not found: {filename}")
                return [], errors
            
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                    try:
                        name = row.get("name", "").strip()
                        username = row.get("github_username", "").strip()
                        email = row.get("email", "").strip()
                        
                        if not name or not username:
                            errors.append(f"Row {row_num}: Missing name or username")
                            continue
                        
                        contributor = Contributor(name, username, email)
                        
                        # Try to restore joined date if available
                        joined_date_str = row.get("joined_date", "").strip()
                        if joined_date_str:
                            try:
                                contributor.joined_date = datetime.fromisoformat(joined_date_str)
                            except ValueError:
                                errors.append(f"Row {row_num}: Invalid date format for {username}")
                        
                        contributors.append(contributor)
                    
                    except Exception as e:
                        errors.append(f"Row {row_num}: Error processing row - {str(e)}")
            
            if contributors:
                print(f"✅ Imported {len(contributors)} contributors from {filename}")
            
            if errors:
                print(f"⚠️  {len(errors)} errors encountered during import:")
                for error in errors[:5]:  # Show first 5 errors
                    print(f"   {error}")
            
            return contributors, errors
        
        except Exception as e:
            errors.append(f"Error reading CSV file: {str(e)}")
            print(f"❌ Error importing contributors: {e}")
            return [], errors
    
    @staticmethod
    def import_contributions_from_csv(contributors_dict: Dict[str, Contributor],
                                     filename: str) -> Tuple[int, List[str]]:
        """
        Import contributions from CSV file and add to contributors.
        
        Args:
            contributors_dict (Dict[str, Contributor]): Dictionary of contributors by username
            filename (str): Input CSV filename
            
        Returns:
            Tuple[int, List[str]]: (number of imported contributions, errors)
        """
        imported_count = 0
        errors = []
        
        try:
            if not os.path.exists(filename):
                errors.append(f"File not found: {filename}")
                return 0, errors
            
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        username = row.get("github_username", "").strip()
                        repo_name = row.get("repo_name", "").strip()
                        contrib_type = row.get("contribution_type", "").strip()
                        description = row.get("description", "").strip()
                        pr_number = row.get("pr_number", "").strip()
                        date_str = row.get("date", "").strip()
                        
                        if not username or not repo_name or not contrib_type or not description:
                            errors.append(f"Row {row_num}: Missing required fields")
                            continue
                        
                        if username not in contributors_dict:
                            errors.append(f"Row {row_num}: Contributor {username} not found")
                            continue
                        
                        # Convert PR number if provided
                        pr_num = None
                        if pr_number:
                            try:
                                pr_num = int(pr_number)
                            except ValueError:
                                errors.append(f"Row {row_num}: Invalid PR number format")
                        
                        contributor = contributors_dict[username]
                        contributor.add_contribution(repo_name, contrib_type, description, pr_num)
                        
                        # Restore date if available
                        if date_str and contributor.contributions:
                            try:
                                contributor.contributions[-1]["date"] = date_str
                            except (ValueError, IndexError):
                                pass
                        
                        imported_count += 1
                    
                    except Exception as e:
                        errors.append(f"Row {row_num}: Error processing row - {str(e)}")
            
            if imported_count > 0:
                print(f"✅ Imported {imported_count} contributions from {filename}")
            
            if errors:
                print(f"⚠️  {len(errors)} errors encountered during import:")
                for error in errors[:5]:
                    print(f"   {error}")
            
            return imported_count, errors
        
        except Exception as e:
            errors.append(f"Error reading CSV file: {str(e)}")
            print(f"❌ Error importing contributions: {e}")
            return 0, errors
    
    @staticmethod
    def import_all_from_csv(contributors_file: str,
                           contributions_file: str,
                           output_dir: str = "imports") -> Tuple[Dict[str, Contributor], List[str]]:
        """
        Import all data from CSV files.
        
        Args:
            contributors_file (str): Contributors CSV filename
            contributions_file (str): Contributions CSV filename
            output_dir (str): Directory containing the files (optional)
            
        Returns:
            Tuple[Dict[str, Contributor], List[str]]: (contributors_dict, all_errors)
        """
        all_errors = []
        
        # Build full paths if output_dir is provided
        if output_dir:
            contributors_file = os.path.join(output_dir, contributors_file)
            contributions_file = os.path.join(output_dir, contributions_file)
        
        # Import contributors
        contributors, contrib_errors = CSVHandler.import_contributors_from_csv(contributors_file)
        all_errors.extend(contrib_errors)
        
        # Create dictionary of contributors
        contributors_dict = {c.github_username: c for c in contributors}
        
        # Import contributions
        contrib_count, import_errors = CSVHandler.import_contributions_from_csv(
            contributors_dict, contributions_file
        )
        all_errors.extend(import_errors)
        
        if contributors:
            print(f"\n✅ Import complete: {len(contributors)} contributors, {contrib_count} contributions")
        
        return contributors_dict, all_errors
    
    @staticmethod
    def get_csv_template(template_type: str = "contributors") -> str:
        """
        Get a CSV template as string.
        
        Args:
            template_type (str): Type of template ("contributors" or "contributions")
            
        Returns:
            str: CSV template
        """
        if template_type == "contributors":
            lines = [",".join(CSVHandler.CONTRIBUTORS_HEADER)]
            lines.append("John Doe,johndoe,john@example.com,2025-10-01,4,Yes")
            lines.append("Jane Smith,janesmith,jane@example.com,2025-10-02,3,No")
            return "\n".join(lines)
        
        elif template_type == "contributions":
            lines = [",".join(CSVHandler.CONTRIBUTIONS_HEADER)]
            lines.append("johndoe,John Doe,my-repo,bug-fix,Fixed login issue,123,2025-10-05")
            lines.append("janesmith,Jane Smith,other-repo,feature,Added new feature,124,2025-10-06")
            return "\n".join(lines)
        
        return ""
    
    @staticmethod
    def save_csv_template(template_type: str = "contributors",
                         filename: str = None) -> bool:
        """
        Save a CSV template to file.
        
        Args:
            template_type (str): Type of template
            filename (str): Output filename (auto-generated if not provided)
            
        Returns:
            bool: True if successful
        """
        if not filename:
            filename = f"{template_type}_template.csv"
        
        try:
            template = CSVHandler.get_csv_template(template_type)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(template)
            print(f"✅ Template saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving template: {e}")
            return False
