"""
Advanced Search Engine for Hacktoberfest 2025 Project Tracker.
Provides comprehensive search and filtering capabilities.
"""

import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from .contributor import Contributor


class SearchType(Enum):
    """Types of search operations."""
    EXACT = "exact"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    REGEX = "regex"
    FUZZY = "fuzzy"


class SortOrder(Enum):
    """Sort order options."""
    ASCENDING = "asc"
    DESCENDING = "desc"


class SearchEngine:
    """Advanced search and filtering engine for contributors and contributions."""
    
    def __init__(self):
        """Initialize the search engine."""
        self.search_history: List[Dict[str, Any]] = []
    
    def search_contributors(self,
                           contributors: List[Contributor],
                           query: str = "",
                           search_type: SearchType = SearchType.CONTAINS,
                           search_field: str = "all",
                           case_sensitive: bool = False) -> List[Contributor]:
        """
        Search contributors with various criteria.
        
        Args:
            contributors (List[Contributor]): List of contributors to search
            query (str): Search query string
            search_type (SearchType): Type of search
            search_field (str): Field to search in ('name', 'username', 'email', 'all')
            case_sensitive (bool): Whether search is case-sensitive
            
        Returns:
            List[Contributor]: Matching contributors
        """
        if not query:
            return contributors
        
        results = []
        
        for contributor in contributors:
            if self._matches_contributor(contributor, query, search_type, search_field, case_sensitive):
                results.append(contributor)
        
        return results
    
    def _matches_contributor(self,
                            contributor: Contributor,
                            query: str,
                            search_type: SearchType,
                            search_field: str,
                            case_sensitive: bool) -> bool:
        """Check if a contributor matches the search criteria."""
        search_query = query if case_sensitive else query.lower()
        
        fields_to_search = []
        
        if search_field in ["name", "all"]:
            fields_to_search.append(contributor.name if case_sensitive else contributor.name.lower())
        
        if search_field in ["username", "all"]:
            fields_to_search.append(contributor.github_username if case_sensitive else contributor.github_username.lower())
        
        if search_field in ["email", "all"]:
            fields_to_search.append(contributor.email if case_sensitive else contributor.email.lower())
        
        for field_value in fields_to_search:
            if self._matches_query(field_value, search_query, search_type):
                return True
        
        return False
    
    @staticmethod
    def _matches_query(text: str, query: str, search_type: SearchType) -> bool:
        """Check if text matches the query based on search type."""
        try:
            if search_type == SearchType.EXACT:
                return text == query
            elif search_type == SearchType.CONTAINS:
                return query in text
            elif search_type == SearchType.STARTS_WITH:
                return text.startswith(query)
            elif search_type == SearchType.ENDS_WITH:
                return text.endswith(query)
            elif search_type == SearchType.REGEX:
                return bool(re.search(query, text))
            elif search_type == SearchType.FUZZY:
                return SearchEngine._fuzzy_match(text, query)
            return False
        except (re.error, TypeError):
            return False
    
    @staticmethod
    def _fuzzy_match(text: str, pattern: str) -> bool:
        """
        Fuzzy string matching.
        Returns True if pattern characters appear in text in order.
        """
        pattern_idx = 0
        for char in text:
            if pattern_idx < len(pattern) and char.lower() == pattern[pattern_idx].lower():
                pattern_idx += 1
        return pattern_idx == len(pattern)
    
    def filter_contributors(self,
                           contributors: List[Contributor],
                           min_contributions: int = None,
                           max_contributions: int = None,
                           completed_only: bool = False,
                           has_email: bool = None,
                           joined_after: datetime = None,
                           joined_before: datetime = None,
                           contribution_type: str = None) -> List[Contributor]:
        """
        Filter contributors by various criteria.
        
        Args:
            contributors (List[Contributor]): List of contributors
            min_contributions (int): Minimum contributions
            max_contributions (int): Maximum contributions
            completed_only (bool): Only return Hacktoberfest completers
            has_email (bool): Must have email
            joined_after (datetime): Joined after this date
            joined_before (datetime): Joined before this date
            contribution_type (str): Must have this contribution type
            
        Returns:
            List[Contributor]: Filtered contributors
        """
        results = contributors
        
        if min_contributions is not None:
            results = [c for c in results if c.get_contribution_count() >= min_contributions]
        
        if max_contributions is not None:
            results = [c for c in results if c.get_contribution_count() <= max_contributions]
        
        if completed_only:
            results = [c for c in results if c.is_hacktoberfest_complete()]
        
        if has_email is not None:
            if has_email:
                results = [c for c in results if c.email]
            else:
                results = [c for c in results if not c.email]
        
        if joined_after:
            results = [c for c in results if c.joined_date >= joined_after]
        
        if joined_before:
            results = [c for c in results if c.joined_date <= joined_before]
        
        if contribution_type:
            results = [c for c in results 
                      if any(contrib.get("type") == contribution_type for contrib in c.contributions)]
        
        return results
    
    def search_contributions(self,
                            contributors: List[Contributor],
                            query: str = "",
                            search_in: str = "all",
                            case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Search across all contributions.
        
        Args:
            contributors (List[Contributor]): List of contributors
            query (str): Search query
            search_in (str): Search in ('description', 'repo', 'type', 'all')
            case_sensitive (bool): Case-sensitive search
            
        Returns:
            List[Dict[str, Any]]: Matching contributions with contributor info
        """
        results = []
        search_query = query if case_sensitive else query.lower()
        
        for contributor in contributors:
            for contrib in contributor.contributions:
                if self._matches_contribution(contrib, search_query, search_in, case_sensitive):
                    result = contrib.copy()
                    result["contributor_name"] = contributor.name
                    result["contributor_username"] = contributor.github_username
                    results.append(result)
        
        return results
    
    def _matches_contribution(self,
                             contrib: Dict[str, Any],
                             query: str,
                             search_in: str,
                             case_sensitive: bool) -> bool:
        """Check if a contribution matches the search."""
        fields = []
        
        if search_in in ["description", "all"]:
            desc = contrib.get("description", "")
            fields.append(desc if case_sensitive else desc.lower())
        
        if search_in in ["repo", "all"]:
            repo = contrib.get("repo_name", "")
            fields.append(repo if case_sensitive else repo.lower())
        
        if search_in in ["type", "all"]:
            ctype = contrib.get("type", "")
            fields.append(ctype if case_sensitive else ctype.lower())
        
        return any(query in field for field in fields)
    
    def filter_contributions(self,
                            contributors: List[Contributor],
                            contribution_type: str = None,
                            repo_name: str = None,
                            after_date: datetime = None,
                            before_date: datetime = None,
                            has_pr: bool = None,
                            contributor_username: str = None) -> List[Dict[str, Any]]:
        """
        Filter contributions by criteria.
        
        Args:
            contributors (List[Contributor]): List of contributors
            contribution_type (str): Filter by type
            repo_name (str): Filter by repository
            after_date (datetime): Contributions after this date
            before_date (datetime): Contributions before this date
            has_pr (bool): Has PR number
            contributor_username (str): From specific contributor
            
        Returns:
            List[Dict[str, Any]]: Filtered contributions
        """
        results = []
        
        for contributor in contributors:
            # Filter by contributor if specified
            if contributor_username and contributor.github_username != contributor_username:
                continue
            
            for contrib in contributor.contributions:
                # Check type
                if contribution_type and contrib.get("type") != contribution_type:
                    continue
                
                # Check repository
                if repo_name and contrib.get("repo_name") != repo_name:
                    continue
                
                # Check date range
                try:
                    contrib_date = datetime.fromisoformat(contrib.get("date", ""))
                    if after_date and contrib_date < after_date:
                        continue
                    if before_date and contrib_date > before_date:
                        continue
                except (ValueError, TypeError):
                    pass
                
                # Check PR
                if has_pr is not None:
                    has_pr_num = bool(contrib.get("pr_number"))
                    if has_pr != has_pr_num:
                        continue
                
                # Add to results
                result = contrib.copy()
                result["contributor_name"] = contributor.name
                result["contributor_username"] = contributor.github_username
                results.append(result)
        
        return results
    
    def get_statistics(self, contributors: List[Contributor]) -> Dict[str, Any]:
        """
        Get search and filter statistics.
        
        Args:
            contributors (List[Contributor]): List of contributors
            
        Returns:
            Dict[str, Any]: Statistics
        """
        all_contributions = []
        for c in contributors:
            all_contributions.extend(c.contributions)
        
        stats = {
            "total_contributors": len(contributors),
            "total_contributions": len(all_contributions),
            "contribution_types": self._count_types(all_contributions),
            "repositories": self._count_repositories(all_contributions),
            "contributors_with_email": sum(1 for c in contributors if c.email),
            "completed_hacktoberfest": sum(1 for c in contributors if c.is_hacktoberfest_complete()),
        }
        
        return stats
    
    @staticmethod
    def _count_types(contributions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count contributions by type."""
        counts = {}
        for contrib in contributions:
            ctype = contrib.get("type", "unknown")
            counts[ctype] = counts.get(ctype, 0) + 1
        return counts
    
    @staticmethod
    def _count_repositories(contributions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count contributions by repository."""
        counts = {}
        for contrib in contributions:
            repo = contrib.get("repo_name", "unknown")
            counts[repo] = counts.get(repo, 0) + 1
        return counts
    
    def sort_contributors(self,
                         contributors: List[Contributor],
                         sort_by: str = "name",
                         order: SortOrder = SortOrder.ASCENDING) -> List[Contributor]:
        """
        Sort contributors by various criteria.
        
        Args:
            contributors (List[Contributor]): List of contributors
            sort_by (str): Field to sort by ('name', 'username', 'contributions', 'joined_date')
            order (SortOrder): Sort order
            
        Returns:
            List[Contributor]: Sorted contributors
        """
        reverse = order == SortOrder.DESCENDING
        
        if sort_by == "name":
            return sorted(contributors, key=lambda c: c.name.lower(), reverse=reverse)
        elif sort_by == "username":
            return sorted(contributors, key=lambda c: c.github_username.lower(), reverse=reverse)
        elif sort_by == "contributions":
            return sorted(contributors, key=lambda c: c.get_contribution_count(), reverse=reverse)
        elif sort_by == "joined_date":
            return sorted(contributors, key=lambda c: c.joined_date, reverse=reverse)
        
        return contributors
    
    def advanced_search(self,
                       contributors: List[Contributor],
                       filters: Dict[str, Any],
                       sort_by: str = "name",
                       sort_order: SortOrder = SortOrder.ASCENDING) -> List[Contributor]:
        """
        Perform an advanced search with multiple filters.
        
        Args:
            contributors (List[Contributor]): List of contributors
            filters (Dict[str, Any]): Filter dictionary with keys like:
                - 'query': Search query
                - 'search_field': Field to search in
                - 'search_type': Type of search
                - 'min_contributions': Minimum contributions
                - 'max_contributions': Maximum contributions
                - 'completed_only': Only completed
                - 'has_email': Must have email
                - 'joined_after': Date filter
                - 'joined_before': Date filter
            sort_by (str): Field to sort by
            sort_order (SortOrder): Sort order
            
        Returns:
            List[Contributor]: Filtered and sorted contributors
        """
        results = contributors
        
        # Apply search
        if filters.get("query"):
            results = self.search_contributors(
                results,
                filters["query"],
                SearchType(filters.get("search_type", "contains")),
                filters.get("search_field", "all"),
                filters.get("case_sensitive", False)
            )
        
        # Apply filters
        results = self.filter_contributors(
            results,
            filters.get("min_contributions"),
            filters.get("max_contributions"),
            filters.get("completed_only", False),
            filters.get("has_email"),
            filters.get("joined_after"),
            filters.get("joined_before"),
            filters.get("contribution_type")
        )
        
        # Apply sorting
        results = self.sort_contributors(results, sort_by, sort_order)
        
        return results
    
    def get_quick_stats(self, search_results: List[Contributor]) -> Dict[str, Any]:
        """
        Get quick statistics for search results.
        
        Args:
            search_results (List[Contributor]): Search results
            
        Returns:
            Dict[str, Any]: Statistics
        """
        total_contrib = sum(c.get_contribution_count() for c in search_results)
        completed = sum(1 for c in search_results if c.is_hacktoberfest_complete())
        
        return {
            "result_count": len(search_results),
            "total_contributions": total_contrib,
            "completed_count": completed,
            "average_contributions": total_contrib / len(search_results) if search_results else 0,
            "completion_rate": (completed / len(search_results) * 100) if search_results else 0,
        }
