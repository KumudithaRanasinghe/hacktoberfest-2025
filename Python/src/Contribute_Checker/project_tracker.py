"""
Project tracker for managing Hacktoberfest contributions and contributors.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from .contributor import Contributor
from .email_notifier import EmailNotifier


class ProjectTracker:
    """Manages the overall Hacktoberfest project and tracks all contributors."""
    
    def __init__(self, project_name: str = "Hacktoberfest 2025", data_file: str = "contributors.json",
                 enable_notifications: bool = False, smtp_server: str = None, 
                 sender_email: str = None, sender_password: str = None):
        """
        Initialize the project tracker.
        
        Args:
            project_name (str): Name of the project
            data_file (str): File to store contributor data
            enable_notifications (bool): Enable email notifications
            smtp_server (str, optional): SMTP server address
            sender_email (str, optional): Email to send from
            sender_password (str, optional): Email password
        """
        self.project_name = project_name
        self.data_file = data_file
        self.contributors: Dict[str, Contributor] = {}
        self.created_date = datetime.now()
        self.enable_notifications = enable_notifications
        
        # Initialize email notifier if enabled
        self.notifier: Optional[EmailNotifier] = None
        if enable_notifications:
            self.notifier = EmailNotifier(
                smtp_server=smtp_server,
                sender_email=sender_email,
                sender_password=sender_password
            )
        
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
        
        # Send welcome email if enabled
        if self.notifier and email:
            self.notifier.send_welcome_email(email, name, github_username)
        
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
        
        # Send milestone notification if enabled
        if self.notifier and contributor.email:
            contribution_count = contributor.get_contribution_count()
            is_complete = contributor.is_hacktoberfest_complete()
            
            # Notify on every contribution or on completion
            if contribution_count % 1 == 0:  # Notify on each contribution
                self.notifier.send_milestone_notification(
                    contributor.email,
                    github_username,
                    contribution_count,
                    is_complete
                )
        
        self.save_data()
        return True
    
    def get_all_contributors(self) -> List[Contributor]:
        """Get a list of all contributors."""
        return list(self.contributors.values())
    
    def get_completed_contributors(self) -> List[Contributor]:
        """Get contributors who have completed Hacktoberfest (4+ contributions)."""
        return [contrib for contrib in self.contributors.values() if contrib.is_hacktoberfest_complete()]
    
    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Get contributors sorted by number of contributions (descending) with additional stats."""
        contributors_with_stats = []
        
        for contributor in self.contributors.values():
            unique_repos = set()
            latest_contribution = None
            
            for contribution in contributor.contributions:
                unique_repos.add(contribution.get('repo_name', ''))
                contrib_date = contribution.get('date', '')
                if not latest_contribution or contrib_date > latest_contribution:
                    latest_contribution = contrib_date
            
            contributors_with_stats.append({
                'name': contributor.name,
                'github_username': contributor.github_username,
                'email': contributor.email,
                'contribution_count': contributor.get_contribution_count(),
                'unique_repositories': len(unique_repos),
                'latest_contribution': latest_contribution,
                'joined_date': contributor.joined_date.isoformat() if contributor.joined_date else None
            })
        
        # Sort by contribution count (descending)
        return sorted(contributors_with_stats, key=lambda x: x['contribution_count'], reverse=True)
    
    def get_project_stats(self) -> Dict[str, Any]:
        """Get overall project statistics."""
        contributors = self.get_all_contributors()
        total_contributions = sum(c.get_contribution_count() for c in contributors)
        completed_count = len(self.get_completed_contributors())
        
        # Get contribution types distribution
        contributions_by_type = {}
        unique_repositories = set()
        
        for contributor in contributors:
            for contribution in contributor.contributions:
                # Track contribution types
                contrib_type = contribution.get('type', 'unknown')
                contributions_by_type[contrib_type] = contributions_by_type.get(contrib_type, 0) + 1
                
                # Track unique repositories
                unique_repositories.add(contribution.get('repo_name', ''))
        
        return {
            "project_name": self.project_name,
            "total_contributors": len(contributors),
            "total_contributions": total_contributions,
            "completed_hacktoberfest": completed_count,
            "completion_rate": f"{(completed_count / len(contributors) * 100):.1f}%" if contributors else "0%",
            "avg_contributions_per_contributor": total_contributions / len(contributors) if contributors else 0,
            "unique_repositories": len(unique_repositories),
            "contributions_by_type": contributions_by_type,
            "created_date": self.created_date.isoformat()
        }
    
    def get_recent_contributions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent contributions across all contributors."""
        all_contributions = []
        
        for contributor in self.contributors.values():
            for contribution in contributor.contributions:
                contribution_data = contribution.copy()
                contribution_data['contributor'] = contributor
                all_contributions.append(contribution_data)
        
        # Sort by date (most recent first)
        all_contributions.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return all_contributions[:limit]
    
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
    
    def send_notification_to_contributor(self, github_username: str) -> bool:
        """
        Manually send a notification to a specific contributor.
        
        Args:
            github_username (str): GitHub username of the contributor
            
        Returns:
            bool: True if notification sent successfully
        """
        if not self.notifier:
            print("❌ Email notifications are not enabled.")
            return False
        
        contributor = self.get_contributor(github_username)
        if not contributor:
            print(f"❌ Contributor {github_username} not found.")
            return False
        
        if not contributor.email:
            print(f"❌ No email address for contributor {github_username}.")
            return False
        
        return self.notifier.send_milestone_notification(
            contributor.email,
            github_username,
            contributor.get_contribution_count(),
            contributor.is_hacktoberfest_complete()
        )
    
    def send_notifications_to_all_contributors(self) -> Dict[str, bool]:
        """
        Send notifications to all contributors.
        
        Returns:
            Dict[str, bool]: Dictionary of (username, success) pairs
        """
        if not self.notifier:
            print("❌ Email notifications are not enabled.")
            return {}
        
        results = {}
        for contributor in self.get_all_contributors():
            if contributor.email:
                results[contributor.github_username] = self.notifier.send_milestone_notification(
                    contributor.email,
                    contributor.github_username,
                    contributor.get_contribution_count(),
                    contributor.is_hacktoberfest_complete()
                )
        
        return results
    
    def get_notification_history(self) -> List[Dict]:
        """
        Get the history of sent notifications.
        
        Returns:
            List[Dict]: List of notification records
        """
        if not self.notifier:
            return []
        
        return self.notifier.get_notification_history()
    
    def enable_email_notifications(self, smtp_server: str = None,
                                  sender_email: str = None,
                                  sender_password: str = None) -> bool:
        """
        Enable email notifications for the project.
        
        Args:
            smtp_server (str, optional): SMTP server address
            sender_email (str, optional): Email to send from
            sender_password (str, optional): Email password
            
        Returns:
            bool: True if notifier initialized successfully
        """
        try:
            self.notifier = EmailNotifier(
                smtp_server=smtp_server,
                sender_email=sender_email,
                sender_password=sender_password
            )
            self.enable_notifications = True
            print("✅ Email notifications enabled successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to enable email notifications: {e}")
            return False
    
    def __str__(self) -> str:
        """String representation of the project tracker."""
        return f"ProjectTracker('{self.project_name}', {len(self.contributors)} contributors)"