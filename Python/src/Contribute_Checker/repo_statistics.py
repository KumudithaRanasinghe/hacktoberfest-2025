"""
Repository Statistics and Analytics for Hacktoberfest 2025 Project Tracker.
Provides comprehensive repository-level metrics and insights.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
import statistics
from .contributor import Contributor


class RepositoryStats:
    """Analytics and statistics for individual repositories."""
    
    def __init__(self):
        """Initialize the repository statistics engine."""
        self.repo_cache: Dict[str, Dict[str, Any]] = {}
    
    def calculate_repository_stats(self,
                                   contributors: List[Contributor],
                                   repo_name: str) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics for a repository.
        
        Args:
            contributors (List[Contributor]): All contributors
            repo_name (str): Repository name to analyze
            
        Returns:
            Dict[str, Any]: Repository statistics
        """
        repo_contributions = []
        repo_contributors = set()
        contribution_types = defaultdict(int)
        dates = []
        pull_requests = []
        
        # Collect all contributions for this repo
        for contributor in contributors:
            for contrib in contributor.contributions:
                if contrib.get("repo_name") == repo_name:
                    repo_contributions.append({
                        "contributor": contributor,
                        "data": contrib
                    })
                    repo_contributors.add(contributor.github_username)
                    contribution_types[contrib.get("type", "unknown")] += 1
                    
                    # Parse date
                    try:
                        contrib_date = datetime.fromisoformat(contrib.get("date", ""))
                        dates.append(contrib_date)
                    except (ValueError, TypeError):
                        pass
                    
                    # Track PRs
                    if contrib.get("pr_number"):
                        pull_requests.append(contrib.get("pr_number"))
        
        # Calculate statistics
        total_contributions = len(repo_contributions)
        unique_contributors = len(repo_contributors)
        avg_contributions_per_contributor = (
            total_contributions / unique_contributors if unique_contributors > 0 else 0
        )
        
        # Date range
        date_range = self._calculate_date_range(dates)
        
        # Contribution timeline
        timeline = self._create_contribution_timeline(dates)
        
        # Top contributors
        top_contributors = self._get_top_contributors(repo_contributions, repo_name)
        
        # Activity score
        activity_score = self._calculate_activity_score(
            total_contributions,
            unique_contributors,
            len(pull_requests),
            len(dates)
        )
        
        stats = {
            "repo_name": repo_name,
            "total_contributions": total_contributions,
            "unique_contributors": unique_contributors,
            "avg_contributions_per_contributor": avg_contributions_per_contributor,
            "contribution_types": dict(contribution_types),
            "pull_requests_count": len(pull_requests),
            "pull_request_percentage": (len(pull_requests) / total_contributions * 100) if total_contributions > 0 else 0,
            "date_range": date_range,
            "first_contribution": dates[0].strftime("%Y-%m-%d") if dates else None,
            "last_contribution": dates[-1].strftime("%Y-%m-%d") if dates else None,
            "days_active": date_range["days_active"],
            "contribution_frequency": self._calculate_frequency(total_contributions, date_range["days_active"]),
            "timeline": timeline,
            "top_contributors": top_contributors,
            "contributor_list": list(repo_contributors),
            "activity_score": activity_score,
            "health_status": self._assess_health_status(
                total_contributions,
                unique_contributors,
                activity_score,
                len(pull_requests)
            ),
        }
        
        # Cache the stats
        self.repo_cache[repo_name] = stats
        
        return stats
    
    def get_all_repositories_stats(self, contributors: List[Contributor]) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics for all repositories.
        
        Args:
            contributors (List[Contributor]): All contributors
            
        Returns:
            Dict[str, Dict[str, Any]]: Statistics for each repository
        """
        repos = set()
        
        # Collect all unique repositories
        for contributor in contributors:
            for contrib in contributor.contributions:
                repos.add(contrib.get("repo_name", "unknown"))
        
        # Calculate stats for each repo
        all_stats = {}
        for repo in repos:
            all_stats[repo] = self.calculate_repository_stats(contributors, repo)
        
        return all_stats
    
    def get_top_repositories(self,
                            contributors: List[Contributor],
                            limit: int = 10,
                            sort_by: str = "contributions") -> List[Tuple[str, Dict[str, Any]]]:
        """
        Get top repositories by various metrics.
        
        Args:
            contributors (List[Contributor]): All contributors
            limit (int): Number of repositories to return
            sort_by (str): Sort criterion ('contributions', 'contributors', 'activity_score', 'pull_requests')
            
        Returns:
            List[Tuple[str, Dict[str, Any]]]: Top repositories with stats
        """
        all_stats = self.get_all_repositories_stats(contributors)
        
        # Sort based on criterion
        if sort_by == "contributions":
            sorted_repos = sorted(
                all_stats.items(),
                key=lambda x: x[1]["total_contributions"],
                reverse=True
            )
        elif sort_by == "contributors":
            sorted_repos = sorted(
                all_stats.items(),
                key=lambda x: x[1]["unique_contributors"],
                reverse=True
            )
        elif sort_by == "activity_score":
            sorted_repos = sorted(
                all_stats.items(),
                key=lambda x: x[1]["activity_score"],
                reverse=True
            )
        elif sort_by == "pull_requests":
            sorted_repos = sorted(
                all_stats.items(),
                key=lambda x: x[1]["pull_requests_count"],
                reverse=True
            )
        else:
            sorted_repos = sorted(
                all_stats.items(),
                key=lambda x: x[1]["total_contributions"],
                reverse=True
            )
        
        return sorted_repos[:limit]
    
    def compare_repositories(self,
                           contributors: List[Contributor],
                           repo_names: List[str]) -> Dict[str, Any]:
        """
        Compare multiple repositories side-by-side.
        
        Args:
            contributors (List[Contributor]): All contributors
            repo_names (List[str]): Repository names to compare
            
        Returns:
            Dict[str, Any]: Comparison data
        """
        comparison = {
            "repositories": [],
            "metrics": {}
        }
        
        for repo_name in repo_names:
            stats = self.calculate_repository_stats(contributors, repo_name)
            comparison["repositories"].append(stats)
            
            # Add to comparison metrics
            for key in ["total_contributions", "unique_contributors", "activity_score", 
                       "pull_requests_count", "contribution_frequency"]:
                if key not in comparison["metrics"]:
                    comparison["metrics"][key] = {}
                comparison["metrics"][key][repo_name] = stats.get(key, 0)
        
        # Calculate rankings
        comparison["rankings"] = self._calculate_rankings(comparison["metrics"])
        
        return comparison
    
    def get_trending_repositories(self,
                                 contributors: List[Contributor],
                                 days: int = 7,
                                 limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get trending repositories based on recent activity.
        
        Args:
            contributors (List[Contributor]): All contributors
            days (int): Number of recent days to consider
            limit (int): Number of repositories to return
            
        Returns:
            List[Dict[str, Any]]: Trending repositories
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_repos = defaultdict(list)
        
        # Collect recent contributions
        for contributor in contributors:
            for contrib in contributor.contributions:
                try:
                    contrib_date = datetime.fromisoformat(contrib.get("date", ""))
                    if contrib_date >= cutoff_date:
                        repo = contrib.get("repo_name", "unknown")
                        recent_repos[repo].append({
                            "contributor": contributor,
                            "data": contrib,
                            "date": contrib_date
                        })
                except (ValueError, TypeError):
                    pass
        
        # Calculate trend score for each repo
        trending = []
        for repo, contribs in recent_repos.items():
            trend_score = len(contribs) + len(set(c["contributor"].github_username for c in contribs))
            trending.append({
                "repo_name": repo,
                "recent_contributions": len(contribs),
                "recent_contributors": len(set(c["contributor"].github_username for c in contribs)),
                "trend_score": trend_score,
                "last_activity": max(c["date"] for c in contribs).strftime("%Y-%m-%d %H:%M:%S"),
            })
        
        # Sort by trend score
        trending = sorted(trending, key=lambda x: x["trend_score"], reverse=True)
        
        return trending[:limit]
    
    def get_repository_health(self, contributors: List[Contributor], repo_name: str) -> Dict[str, Any]:
        """
        Assess the health of a repository.
        
        Args:
            contributors (List[Contributor]): All contributors
            repo_name (str): Repository name
            
        Returns:
            Dict[str, Any]: Health assessment
        """
        stats = self.calculate_repository_stats(contributors, repo_name)
        
        health = {
            "overall_score": 0,
            "status": "healthy",
            "metrics": {},
            "recommendations": [],
            "warnings": []
        }
        
        score = 0
        
        # Contribution volume check
        contrib_vol = stats["total_contributions"]
        if contrib_vol >= 50:
            score += 25
            health["metrics"]["contribution_volume"] = "excellent"
        elif contrib_vol >= 20:
            score += 15
            health["metrics"]["contribution_volume"] = "good"
        elif contrib_vol >= 5:
            score += 10
            health["metrics"]["contribution_volume"] = "fair"
        else:
            health["metrics"]["contribution_volume"] = "low"
            health["warnings"].append("Low contribution volume")
        
        # Contributor diversity
        contributors_count = stats["unique_contributors"]
        if contributors_count >= 10:
            score += 25
            health["metrics"]["contributor_diversity"] = "excellent"
        elif contributors_count >= 5:
            score += 15
            health["metrics"]["contributor_diversity"] = "good"
        elif contributors_count >= 2:
            score += 10
            health["metrics"]["contributor_diversity"] = "fair"
        else:
            health["metrics"]["contributor_diversity"] = "low"
            health["warnings"].append("Few unique contributors")
        
        # PR activity
        pr_percentage = stats["pull_request_percentage"]
        if pr_percentage >= 50:
            score += 25
            health["metrics"]["pr_activity"] = "excellent"
        elif pr_percentage >= 30:
            score += 15
            health["metrics"]["pr_activity"] = "good"
        elif pr_percentage >= 10:
            score += 10
            health["metrics"]["pr_activity"] = "fair"
        else:
            health["metrics"]["pr_activity"] = "low"
            health["warnings"].append("Low PR activity")
        
        # Activity consistency
        activity_score = stats["activity_score"]
        if activity_score >= 75:
            score += 25
            health["metrics"]["activity_consistency"] = "excellent"
        elif activity_score >= 50:
            score += 15
            health["metrics"]["activity_consistency"] = "good"
        elif activity_score >= 25:
            score += 10
            health["metrics"]["activity_consistency"] = "fair"
        else:
            health["metrics"]["activity_consistency"] = "low"
            health["warnings"].append("Inconsistent activity")
        
        health["overall_score"] = score
        
        # Set status
        if score >= 80:
            health["status"] = "healthy"
            health["recommendations"].append("Repository is performing well!")
        elif score >= 50:
            health["status"] = "moderate"
            health["recommendations"].append("Consider increasing contributor engagement")
        else:
            health["status"] = "needs_attention"
            health["recommendations"].append("Repository needs increased activity and contributor engagement")
        
        return health
    
    @staticmethod
    def _calculate_date_range(dates: List[datetime]) -> Dict[str, Any]:
        """Calculate date range statistics."""
        if not dates:
            return {
                "start_date": None,
                "end_date": None,
                "days_active": 0,
                "days_span": 0
            }
        
        dates_sorted = sorted(dates)
        start = dates_sorted[0]
        end = dates_sorted[-1]
        days_span = (end - start).days + 1
        
        # Count days with at least one contribution
        unique_dates = set(d.date() for d in dates)
        days_active = len(unique_dates)
        
        return {
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
            "days_active": days_active,
            "days_span": days_span
        }
    
    @staticmethod
    def _create_contribution_timeline(dates: List[datetime]) -> Dict[str, int]:
        """Create a timeline of contributions by date."""
        timeline = defaultdict(int)
        for date in dates:
            date_key = date.strftime("%Y-%m-%d")
            timeline[date_key] += 1
        return dict(sorted(timeline.items()))
    
    @staticmethod
    def _get_top_contributors(contributions: List[Dict], repo_name: str) -> List[Dict[str, Any]]:
        """Get top contributors for a repository."""
        contributor_counts = defaultdict(int)
        
        for item in contributions:
            username = item["contributor"].github_username
            contributor_counts[username] += 1
        
        # Sort by contribution count
        sorted_contributors = sorted(
            contributor_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                "username": username,
                "contributions": count,
                "percentage": (count / len(contributions) * 100) if contributions else 0
            }
            for username, count in sorted_contributors[:5]
        ]
    
    @staticmethod
    def _calculate_activity_score(total_contrib: int,
                                  unique_contributors: int,
                                  pr_count: int,
                                  days_active: int) -> float:
        """
        Calculate an activity score (0-100).
        Considers volume, diversity, PRs, and consistency.
        """
        score = 0
        
        # Contribution volume (max 30 points)
        if total_contrib >= 50:
            score += 30
        elif total_contrib >= 20:
            score += 20
        elif total_contrib >= 5:
            score += 10
        else:
            score += max(0, (total_contrib / 5) * 10)
        
        # Contributor diversity (max 30 points)
        if unique_contributors >= 10:
            score += 30
        elif unique_contributors >= 5:
            score += 20
        elif unique_contributors >= 2:
            score += 10
        else:
            score += 5
        
        # PR engagement (max 25 points)
        if total_contrib > 0:
            pr_percentage = (pr_count / total_contrib) * 100
            score += min(25, (pr_percentage / 100) * 25)
        
        # Days active (max 15 points)
        if days_active >= 30:
            score += 15
        elif days_active >= 14:
            score += 10
        elif days_active >= 7:
            score += 5
        
        return min(100, score)
    
    @staticmethod
    def _calculate_frequency(total_contrib: int, days_active: int) -> float:
        """Calculate contribution frequency (contributions per day)."""
        if days_active == 0:
            return 0.0
        return round(total_contrib / days_active, 2)
    
    @staticmethod
    def _assess_health_status(total_contrib: int,
                              unique_contributors: int,
                              activity_score: float,
                              pr_count: int) -> str:
        """Assess overall health status."""
        if (total_contrib >= 20 and unique_contributors >= 5 and 
            activity_score >= 60 and pr_count >= 5):
            return "excellent"
        elif (total_contrib >= 10 and unique_contributors >= 3 and 
              activity_score >= 40):
            return "good"
        elif (total_contrib >= 5 and unique_contributors >= 2):
            return "fair"
        else:
            return "needs_attention"
    
    @staticmethod
    def _calculate_rankings(metrics: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, int]]:
        """Calculate rankings for each metric across repositories."""
        rankings = {}
        
        for metric_name, repo_values in metrics.items():
            # Sort repositories by metric value
            ranked = sorted(
                repo_values.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            rankings[metric_name] = {
                repo: rank + 1
                for rank, (repo, _) in enumerate(ranked)
            }
        
        return rankings
