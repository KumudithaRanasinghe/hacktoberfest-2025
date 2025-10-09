"""
Project tracker for managing Hacktoberfest contributions and contributors.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from .contributor import Contributor


class ProjectTracker:
    """Manages the overall Hacktoberfest project and tracks all contributors."""
    
    def __init__(self, project_name: str = "Hacktoberfest 2025", data_file: str = "contributors.json"):
        """
        Initialize the project tracker.
        
        Args:
            project_name (str): Name of the project
            data_file (str): File to store contributor data
        """
        self.project_name = project_name
        self.data_file = data_file
        self.contributors: Dict[str, Contributor] = {}
        self.created_date = datetime.now()
        self.load_data()
    
    def add_contributor(self, name: str, github_username: str, email: str = "") -> Contributor:
        """
        Add a new contributor to the project.
        
        Args:
            name (str): Full name of the contributor
            github_username (str): GitHub username
            email (str, optional): Email address
            
        Returns:
            Contributor: The newly created contributor object
        """
        if github_username in self.contributors:
            return self.contributors[github_username]
        
        contributor = Contributor(name, github_username, email)
        self.contributors[github_username] = contributor
        self.save_data()
        return contributor
    
    def get_contributor(self, github_username: str) -> Optional[Contributor]:
        """
        Get a contributor by their GitHub username.
        
        Args:
            github_username (str): GitHub username to search for
            
        Returns:
            Optional[Contributor]: Contributor object if found, None otherwise
        """
        return self.contributors.get(github_username)
    
    def add_contribution(self, github_username: str, repo_name: str, contribution_type: str, 
                        description: str, pr_number: int = None) -> bool:
        """
        Add a contribution for a specific contributor.
        
        Args:
            github_username (str): GitHub username of the contributor
            repo_name (str): Name of the repository
            contribution_type (str): Type of contribution
            description (str): Description of the contribution
            pr_number (int, optional): Pull request number
            
        Returns:
            bool: True if contribution was added successfully, False otherwise
        """
        contributor = self.get_contributor(github_username)
        if not contributor:
            return False
        
        contributor.add_contribution(repo_name, contribution_type, description, pr_number)
        self.save_data()
        return True
    
    def get_all_contributors(self) -> List[Contributor]:
        """Get a list of all contributors."""
        return list(self.contributors.values())
    
    def get_completed_contributors(self) -> List[Contributor]:
        """Get contributors who have completed Hacktoberfest (4+ contributions)."""
        return [contrib for contrib in self.contributors.values() if contrib.is_hacktoberfest_complete()]
    
    def get_leaderboard(self) -> List[Contributor]:
        """Get contributors sorted by number of contributions (descending)."""
        return sorted(self.contributors.values(), key=lambda c: c.get_contribution_count(), reverse=True)
    
    def get_project_stats(self) -> Dict[str, Any]:
        """Get overall project statistics."""
        contributors = self.get_all_contributors()
        total_contributions = sum(c.get_contribution_count() for c in contributors)
        completed_count = len(self.get_completed_contributors())
        
        return {
            "project_name": self.project_name,
            "total_contributors": len(contributors),
            "total_contributions": total_contributions,
            "completed_hacktoberfest": completed_count,
            "completion_rate": f"{(completed_count / len(contributors) * 100):.1f}%" if contributors else "0%",
            "created_date": self.created_date.isoformat()
        }
    
    def save_data(self) -> None:
        """Save contributor data to JSON file."""
        data = {
            "project_name": self.project_name,
            "created_date": self.created_date.isoformat(),
            "contributors": {username: contrib.to_dict() for username, contrib in self.contributors.items()}
        }
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self) -> None:
        """Load contributor data from JSON file."""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.project_name = data.get("project_name", self.project_name)
            if "created_date" in data:
                self.created_date = datetime.fromisoformat(data["created_date"])
            
            for username, contrib_data in data.get("contributors", {}).items():
                contributor = Contributor(
                    contrib_data["name"],
                    contrib_data["github_username"],
                    contrib_data.get("email", "")
                )
                
                if "joined_date" in contrib_data:
                    contributor.joined_date = datetime.fromisoformat(contrib_data["joined_date"])
                
                contributor.contributions = contrib_data.get("contributions", [])
                self.contributors[username] = contributor
                
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def print_leaderboard(self) -> None:
        """Print a formatted leaderboard of contributors."""
        print(f"\n🎃 {self.project_name} - Leaderboard 🎃")
        print("=" * 50)
        
        leaderboard = self.get_leaderboard()
        if not leaderboard:
            print("No contributors yet!")
            return
        
        for i, contributor in enumerate(leaderboard, 1):
            emoji = "🏆" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "👤"
            print(f"{emoji} {i:2d}. {contributor}")
    
    def print_stats(self) -> None:
        """Print project statistics."""
        stats = self.get_project_stats()
        print(f"\n📊 {stats['project_name']} - Statistics 📊")
        print("=" * 50)
        print(f"Total Contributors: {stats['total_contributors']}")
        print(f"Total Contributions: {stats['total_contributions']}")
        print(f"Completed Hacktoberfest: {stats['completed_hacktoberfest']}")
        print(f"Completion Rate: {stats['completion_rate']}")
        print(f"Project Started: {stats['created_date'][:10]}")
    
    def __str__(self) -> str:
        """String representation of the project tracker."""
        return f"ProjectTracker('{self.project_name}', {len(self.contributors)} contributors)"