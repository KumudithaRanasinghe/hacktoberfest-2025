"""
Performance Metrics Module for Hacktoberfest 2025 Project Tracker.
Provides analytics, statistics, and performance insights for contributors and projects.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
from statistics import mean, median, stdev
from .contributor import Contributor


class PerformanceMetrics:
    """Analyzes and computes performance metrics for Hacktoberfest contributors."""
    
    def __init__(self):
        """Initialize the performance metrics analyzer."""
        self.cache: Dict[str, Any] = {}
        self.cache_timestamp: Optional[datetime] = None
        self.cache_ttl = 300  # Cache time-to-live in seconds
    
    def _invalidate_cache(self) -> None:
        """Invalidate the metrics cache."""
        self.cache.clear()
        self.cache_timestamp = None
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if not self.cache_timestamp:
            return False
        age = (datetime.now() - self.cache_timestamp).total_seconds()
        return age < self.cache_ttl
    
    def calculate_contributor_metrics(self, contributor: Contributor) -> Dict[str, Any]:
        """
        Calculate detailed metrics for a single contributor.
        
        Args:
            contributor (Contributor): Contributor object
            
        Returns:
            Dict[str, Any]: Dictionary containing various metrics
        """
        metrics = {
            "name": contributor.name,
            "username": contributor.github_username,
            "total_contributions": contributor.get_contribution_count(),
            "joined_date": contributor.joined_date.isoformat(),
            "days_active": (datetime.now() - contributor.joined_date).days,
            "contributions_by_type": {},
            "contributions_by_repo": {},
            "contribution_dates": [],
            "average_days_between_contributions": 0.0,
            "most_active_day": None,
            "hacktoberfest_complete": contributor.is_hacktoberfest_complete(),
            "contribution_streak": 0,
        }
        
        if not contributor.contributions:
            return metrics
        
        # Analyze contributions by type
        for contrib in contributor.contributions:
            contrib_type = contrib.get("type", "unknown")
            metrics["contributions_by_type"][contrib_type] = \
                metrics["contributions_by_type"].get(contrib_type, 0) + 1
        
        # Analyze contributions by repository
        for contrib in contributor.contributions:
            repo = contrib.get("repo_name", "unknown")
            metrics["contributions_by_repo"][repo] = \
                metrics["contributions_by_repo"].get(repo, 0) + 1
        
        # Extract and sort contribution dates
        contrib_dates = []
        for contrib in contributor.contributions:
            try:
                date = datetime.fromisoformat(contrib.get("date", ""))
                contrib_dates.append(date)
            except (ValueError, TypeError):
                pass
        
        contrib_dates.sort()
        metrics["contribution_dates"] = [d.isoformat() for d in contrib_dates]
        
        # Calculate days between contributions
        if len(contrib_dates) > 1:
            days_between = []
            for i in range(1, len(contrib_dates)):
                delta = (contrib_dates[i] - contrib_dates[i-1]).days
                if delta > 0:
                    days_between.append(delta)
            
            if days_between:
                metrics["average_days_between_contributions"] = mean(days_between)
        
        # Find most active day of week
        if contrib_dates:
            day_counts = defaultdict(int)
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for date in contrib_dates:
                day_counts[day_names[date.weekday()]] += 1
            metrics["most_active_day"] = max(day_counts, key=day_counts.get) if day_counts else None
        
        # Calculate contribution streak
        metrics["contribution_streak"] = self._calculate_streak(contrib_dates)
        
        return metrics
    
    @staticmethod
    def _calculate_streak(dates: List[datetime]) -> int:
        """
        Calculate the longest contribution streak.
        
        Args:
            dates (List[datetime]): List of contribution dates
            
        Returns:
            int: Length of the longest streak
        """
        if not dates:
            return 0
        
        dates = sorted(set([d.date() for d in dates]))
        
        if not dates:
            return 0
        
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        return max_streak
    
    def calculate_project_metrics(self, contributors: List[Contributor]) -> Dict[str, Any]:
        """
        Calculate overall project performance metrics.
        
        Args:
            contributors (List[Contributor]): List of all contributors
            
        Returns:
            Dict[str, Any]: Dictionary containing project-wide metrics
        """
        if not contributors:
            return {
                "total_contributors": 0,
                "total_contributions": 0,
                "average_contributions_per_contributor": 0.0,
                "median_contributions_per_contributor": 0.0,
                "hacktoberfest_completion_rate": 0.0,
                "contribution_distribution": {},
            }
        
        contribution_counts = [c.get_contribution_count() for c in contributors]
        total_contributions = sum(contribution_counts)
        completed = sum(1 for c in contributors if c.is_hacktoberfest_complete())
        
        metrics = {
            "total_contributors": len(contributors),
            "total_contributions": total_contributions,
            "average_contributions_per_contributor": mean(contribution_counts),
            "median_contributions_per_contributor": median(contribution_counts),
            "contribution_std_dev": stdev(contribution_counts) if len(contribution_counts) > 1 else 0.0,
            "min_contributions": min(contribution_counts),
            "max_contributions": max(contribution_counts),
            "hacktoberfest_completion_rate": (completed / len(contributors) * 100) if contributors else 0.0,
            "completed_contributors": completed,
            "contribution_distribution": self._get_distribution(contribution_counts),
            "top_contributors": [],
            "top_repositories": {},
            "contribution_types_summary": {},
        }
        
        # Get top contributors
        sorted_contributors = sorted(contributors, 
                                    key=lambda c: c.get_contribution_count(), 
                                    reverse=True)
        metrics["top_contributors"] = [
            {
                "name": c.name,
                "username": c.github_username,
                "contributions": c.get_contribution_count()
            }
            for c in sorted_contributors[:10]
        ]
        
        # Get top repositories
        repo_counts = defaultdict(int)
        type_counts = defaultdict(int)
        for contributor in contributors:
            for contrib in contributor.contributions:
                repo_counts[contrib.get("repo_name", "unknown")] += 1
                type_counts[contrib.get("type", "unknown")] += 1
        
        metrics["top_repositories"] = dict(
            sorted(repo_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        metrics["contribution_types_summary"] = dict(type_counts)
        
        return metrics
    
    @staticmethod
    def _get_distribution(values: List[int]) -> Dict[str, int]:
        """
        Get distribution of contribution counts.
        
        Args:
            values (List[int]): List of contribution counts
            
        Returns:
            Dict[str, int]: Distribution buckets
        """
        distribution = {
            "0-1": 0,
            "2-3": 0,
            "4-5": 0,
            "6-10": 0,
            "11-20": 0,
            "21+": 0,
        }
        
        for value in values:
            if value <= 1:
                distribution["0-1"] += 1
            elif value <= 3:
                distribution["2-3"] += 1
            elif value <= 5:
                distribution["4-5"] += 1
            elif value <= 10:
                distribution["6-10"] += 1
            elif value <= 20:
                distribution["11-20"] += 1
            else:
                distribution["21+"] += 1
        
        return distribution
    
    def calculate_time_series_metrics(self, contributors: List[Contributor]) -> Dict[str, Any]:
        """
        Calculate time-series metrics for contribution trends.
        
        Args:
            contributors (List[Contributor]): List of all contributors
            
        Returns:
            Dict[str, Any]: Time-series metrics
        """
        metrics = {
            "daily_contributions": defaultdict(int),
            "weekly_contributions": defaultdict(int),
            "cumulative_contributions": [],
        }
        
        all_contributions = []
        for contributor in contributors:
            all_contributions.extend(contributor.contributions)
        
        if not all_contributions:
            return metrics
        
        # Group by day and week
        for contrib in all_contributions:
            try:
                date = datetime.fromisoformat(contrib.get("date", ""))
                day_key = date.strftime("%Y-%m-%d")
                week_key = date.strftime("%Y-W%U")
                
                metrics["daily_contributions"][day_key] += 1
                metrics["weekly_contributions"][week_key] += 1
            except (ValueError, TypeError):
                pass
        
        # Calculate cumulative contributions
        sorted_days = sorted(metrics["daily_contributions"].keys())
        cumulative = 0
        for day in sorted_days:
            cumulative += metrics["daily_contributions"][day]
            metrics["cumulative_contributions"].append({
                "date": day,
                "total": cumulative
            })
        
        # Convert defaultdicts to regular dicts
        metrics["daily_contributions"] = dict(metrics["daily_contributions"])
        metrics["weekly_contributions"] = dict(metrics["weekly_contributions"])
        
        return metrics
    
    def get_engagement_score(self, contributor: Contributor) -> float:
        """
        Calculate an engagement score for a contributor (0-100).
        
        Factors:
        - Contribution count (40%)
        - Consistency (days active) (30%)
        - Variety of contribution types (20%)
        - Recency (10%)
        
        Args:
            contributor (Contributor): Contributor object
            
        Returns:
            float: Engagement score between 0-100
        """
        if contributor.get_contribution_count() == 0:
            return 0.0
        
        score = 0.0
        
        # Factor 1: Contribution count (0-40 points)
        contrib_score = min(contributor.get_contribution_count() / 4 * 40, 40)
        score += contrib_score
        
        # Factor 2: Days active (0-30 points)
        days_active = (datetime.now() - contributor.joined_date).days
        days_score = min(days_active / 31 * 30, 30)  # Max 30 days
        score += days_score
        
        # Factor 3: Variety of contribution types (0-20 points)
        unique_types = len(contributor.get_contributions_by_type(
            list(set(c["type"] for c in contributor.contributions))[0]
            if contributor.contributions else "unknown"
        ))
        
        type_counts = defaultdict(int)
        for contrib in contributor.contributions:
            type_counts[contrib.get("type", "unknown")] += 1
        variety_score = min(len(type_counts) / 5 * 20, 20)  # Max 5 types
        score += variety_score
        
        # Factor 4: Recency (0-10 points)
        if contributor.contributions:
            try:
                last_contrib = max(
                    datetime.fromisoformat(c.get("date", "")) 
                    for c in contributor.contributions
                )
                days_since_last = (datetime.now() - last_contrib).days
                recency_score = max(10 - (days_since_last / 7), 0)  # Decreases over time
                score += min(recency_score, 10)
            except (ValueError, TypeError):
                pass
        
        return round(score, 2)
    
    def get_contributors_ranking(self, contributors: List[Contributor]) -> List[Dict[str, Any]]:
        """
        Get a ranked list of contributors by engagement score.
        
        Args:
            contributors (List[Contributor]): List of all contributors
            
        Returns:
            List[Dict[str, Any]]: Ranked contributors with scores
        """
        rankings = []
        
        for contributor in contributors:
            score = self.get_engagement_score(contributor)
            rankings.append({
                "rank": 0,  # Will be set after sorting
                "name": contributor.name,
                "username": contributor.github_username,
                "engagement_score": score,
                "contributions": contributor.get_contribution_count(),
                "hacktoberfest_complete": contributor.is_hacktoberfest_complete(),
            })
        
        # Sort by engagement score
        rankings = sorted(rankings, key=lambda x: x["engagement_score"], reverse=True)
        
        # Assign ranks
        for i, ranking in enumerate(rankings, 1):
            ranking["rank"] = i
        
        return rankings
    
    def get_performance_summary(self, contributors: List[Contributor]) -> Dict[str, Any]:
        """
        Get a comprehensive performance summary.
        
        Args:
            contributors (List[Contributor]): List of all contributors
            
        Returns:
            Dict[str, Any]: Comprehensive performance summary
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "contributor_metrics": self.calculate_project_metrics(contributors),
            "time_series": self.calculate_time_series_metrics(contributors),
            "rankings": self.get_contributors_ranking(contributors),
            "individual_metrics": {
                c.github_username: self.calculate_contributor_metrics(c)
                for c in contributors
            },
        }
    
    def get_performance_insights(self, contributors: List[Contributor]) -> Dict[str, Any]:
        """
        Generate insights and recommendations based on performance data.
        
        Args:
            contributors (List[Contributor]): List of all contributors
            
        Returns:
            Dict[str, Any]: Insights and recommendations
        """
        insights = {
            "timestamp": datetime.now().isoformat(),
            "highlights": [],
            "concerns": [],
            "recommendations": [],
            "statistics": {},
        }
        
        if not contributors:
            insights["highlights"].append("No contributors yet. Start recruiting!")
            return insights
        
        project_metrics = self.calculate_project_metrics(contributors)
        
        # Generate highlights
        if project_metrics["hacktoberfest_completion_rate"] >= 80:
            insights["highlights"].append(
                f"🎉 Excellent completion rate: {project_metrics['hacktoberfest_completion_rate']:.1f}%"
            )
        
        if project_metrics["total_contributions"] > 100:
            insights["highlights"].append(
                f"🌟 Outstanding participation: {project_metrics['total_contributions']} total contributions"
            )
        
        if len(project_metrics["top_contributors"]) > 0:
            top = project_metrics["top_contributors"][0]
            insights["highlights"].append(
                f"⭐ Star contributor: {top['name']} with {top['contributions']} contributions"
            )
        
        # Generate concerns
        if project_metrics["hacktoberfest_completion_rate"] < 30:
            insights["concerns"].append(
                f"⚠️  Low completion rate: {project_metrics['hacktoberfest_completion_rate']:.1f}%"
            )
        
        inactive_contributors = sum(
            1 for c in contributors 
            if (datetime.now() - c.joined_date).days > 14 and c.get_contribution_count() < 2
        )
        if inactive_contributors > 0:
            insights["concerns"].append(
                f"😴 {inactive_contributors} contributors may be inactive"
            )
        
        # Generate recommendations
        if project_metrics["average_contributions_per_contributor"] < 2:
            insights["recommendations"].append(
                "Consider creating beginner-friendly issues to boost engagement"
            )
        
        if len(project_metrics["top_repositories"]) == 1:
            insights["recommendations"].append(
                "Diversify contributions across more repositories"
            )
        
        insights["statistics"] = {
            "total_contributors": project_metrics["total_contributors"],
            "completed": project_metrics["completed_contributors"],
            "average_per_contributor": round(project_metrics["average_contributions_per_contributor"], 2),
            "median_per_contributor": round(project_metrics["median_contributions_per_contributor"], 2),
        }
        
        return insights
