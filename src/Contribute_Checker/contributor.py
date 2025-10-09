"""
Contributor class for managing individual contributor information.
"""

from datetime import datetime
from typing import List, Dict, Any


class Contributor:
    """Represents a Hacktoberfest contributor with their information and contributions."""
    
    def __init__(self, name: str, github_username: str, email: str = ""):
        """
        Initialize a new contributor.
        
        Args:
            name (str): Full name of the contributor
            github_username (str): GitHub username
            email (str, optional): Email address
        """
        self.name = name
        self.github_username = github_username
        self.email = email
        self.contributions: List[Dict[str, Any]] = []
        self.joined_date = datetime.now()
    
    def add_contribution(self, repo_name: str, contribution_type: str, description: str, pr_number: int = None):
        """
        Add a new contribution to the contributor's record.
        
        Args:
            repo_name (str): Name of the repository
            contribution_type (str): Type of contribution (e.g., 'bug-fix', 'feature', 'documentation')
            description (str): Description of the contribution
            pr_number (int, optional): Pull request number
        """
        contribution = {
            "repo_name": repo_name,
            "type": contribution_type,
            "description": description,
            "pr_number": pr_number,
            "date": datetime.now().isoformat(),
        }
        self.contributions.append(contribution)
    
    def get_contribution_count(self) -> int:
        """Return the total number of contributions."""
        return len(self.contributions)
    
    def get_contributions_by_type(self, contribution_type: str) -> List[Dict[str, Any]]:
        """
        Get all contributions of a specific type.
        
        Args:
            contribution_type (str): Type of contribution to filter by
            
        Returns:
            List[Dict[str, Any]]: List of contributions matching the type
        """
        return [contrib for contrib in self.contributions if contrib["type"] == contribution_type]
    
    def is_hacktoberfest_complete(self) -> bool:
        """Check if the contributor has completed Hacktoberfest (4+ contributions)."""
        return self.get_contribution_count() >= 4
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert contributor to dictionary representation."""
        return {
            "name": self.name,
            "github_username": self.github_username,
            "email": self.email,
            "joined_date": self.joined_date.isoformat(),
            "contributions": self.contributions,
            "contribution_count": self.get_contribution_count(),
            "hacktoberfest_complete": self.is_hacktoberfest_complete()
        }
    
    def __str__(self) -> str:
        """String representation of the contributor."""
        status = "✅ Complete" if self.is_hacktoberfest_complete() else f"📝 {self.get_contribution_count()}/4"
        return f"{self.name} (@{self.github_username}) - {status}"
    
    def __repr__(self) -> str:
        """Developer representation of the contributor."""
        return f"Contributor(name='{self.name}', github_username='{self.github_username}', contributions={self.get_contribution_count()})"