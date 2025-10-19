"""
Visualization utilities for Hacktoberfest 2025 Performance Metrics.
Provides ASCII-based charts and graphs for terminal display.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class MetricsVisualizer:
    """Creates ASCII visualizations of performance metrics."""
    
    @staticmethod
    def create_bar_chart(data: Dict[str, int], title: str = "", max_width: int = 50) -> str:
        """
        Create a horizontal bar chart.
        
        Args:
            data (Dict[str, int]): Dictionary with labels and values
            title (str): Chart title
            max_width (int): Maximum width of bars
            
        Returns:
            str: ASCII bar chart
        """
        if not data:
            return "No data to display"
        
        output = []
        if title:
            output.append(f"\n{title}")
            output.append("=" * (len(title) + 10))
        
        max_value = max(data.values()) if data.values() else 1
        max_label_len = max(len(str(label)) for label in data.keys())
        
        for label, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
            bar_width = int((value / max_value) * max_width)
            bar = "█" * bar_width
            padding = " " * (max_label_len - len(str(label)))
            output.append(f"{label}{padding} │ {bar} {value}")
        
        return "\n".join(output)
    
    @staticmethod
    def create_progress_bar(current: int, total: int, width: int = 30, label: str = "") -> str:
        """
        Create a progress bar.
        
        Args:
            current (int): Current progress
            total (int): Total
            width (int): Width of the bar
            label (str): Label for the bar
            
        Returns:
            str: ASCII progress bar
        """
        percentage = (current / total * 100) if total > 0 else 0
        filled = int(width * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (width - filled)
        
        result = f"{label}\n" if label else ""
        result += f"[{bar}] {percentage:.1f}% ({current}/{total})"
        
        return result
    
    @staticmethod
    def create_distribution_chart(distribution: Dict[str, int], title: str = "") -> str:
        """
        Create a distribution chart with emoji indicators.
        
        Args:
            distribution (Dict[str, int]): Distribution data
            title (str): Chart title
            
        Returns:
            str: ASCII distribution chart
        """
        output = []
        if title:
            output.append(f"\n{title}")
            output.append("=" * (len(title) + 10))
        
        total = sum(distribution.values())
        
        for key, value in distribution.items():
            percentage = (value / total * 100) if total > 0 else 0
            bar_width = int(percentage / 2)  # Scale to 50 max
            bar = "▓" * bar_width
            
            # Add emoji based on key
            emoji = "🔴"
            if "4-5" in key or "6-10" in key or "11" in key:
                emoji = "🟢"
            elif "2-3" in key:
                emoji = "🟡"
            
            output.append(f"{emoji} {key:>12}: {bar} {percentage:.1f}% ({value})")
        
        return "\n".join(output)
    
    @staticmethod
    def create_time_series_chart(data: Dict[str, int], title: str = "", height: int = 10) -> str:
        """
        Create an ASCII time-series line chart.
        
        Args:
            data (Dict[str, int]): Time series data with dates as keys
            title (str): Chart title
            height (int): Height of the chart
            
        Returns:
            str: ASCII time-series chart
        """
        if not data:
            return "No data to display"
        
        output = []
        if title:
            output.append(f"\n{title}")
            output.append("=" * (len(title) + 10))
        
        # Sort by date
        sorted_data = sorted(data.items())
        values = [v for _, v in sorted_data]
        
        if not values:
            return "No data to display"
        
        max_value = max(values)
        min_value = min(values)
        range_value = max_value - min_value if max_value != min_value else 1
        
        # Create chart rows
        for row in range(height, 0, -1):
            line = ""
            threshold = min_value + (range_value * row / height)
            
            for _, value in sorted_data:
                if value >= threshold:
                    line += "█"
                elif value >= threshold - (range_value / height / 2):
                    line += "▄"
                else:
                    line += " "
            
            output.append(f"{int(threshold):>5} │ {line}")
        
        # Add x-axis
        x_axis = "      └" + "─" * len(sorted_data)
        output.append(x_axis)
        
        # Add date labels (sample)
        labels = ""
        step = max(1, len(sorted_data) // 5)
        for i, (date, _) in enumerate(sorted_data):
            if i % step == 0:
                labels += date[:5]
            else:
                labels += "     "
        output.append(f"        {labels}")
        
        output.append(f"Min: {min_value}, Max: {max_value}")
        
        return "\n".join(output)
    
    @staticmethod
    def create_ranking_table(rankings: List[Dict[str, Any]], top_n: int = 10) -> str:
        """
        Create a ranking table.
        
        Args:
            rankings (List[Dict[str, Any]]): Ranking data
            top_n (int): Number of top entries to show
            
        Returns:
            str: ASCII ranking table
        """
        output = []
        output.append("\n🏆 RANKINGS 🏆")
        output.append("=" * 75)
        output.append(f"{'Rank':<6} {'Name':<20} {'Username':<15} {'Score':<10} {'Status':<15}")
        output.append("-" * 75)
        
        for ranking in rankings[:top_n]:
            medal = "🥇" if ranking['rank'] == 1 else "🥈" if ranking['rank'] == 2 else "🥉" if ranking['rank'] == 3 else "  "
            status = "✅ Complete" if ranking.get('hacktoberfest_complete') else f"📝 {ranking.get('contributions', 0)}/4"
            
            output.append(
                f"{medal} {ranking['rank']:<4} {ranking['name'][:19]:<20} "
                f"{ranking['username']:<15} {ranking['engagement_score']:<10.1f} {status:<15}"
            )
        
        output.append("=" * 75)
        return "\n".join(output)
    
    @staticmethod
    def create_stats_card(stats: Dict[str, Any], title: str = "Statistics") -> str:
        """
        Create a statistics card display.
        
        Args:
            stats (Dict[str, Any]): Statistics dictionary
            title (str): Card title
            
        Returns:
            str: ASCII stats card
        """
        output = []
        output.append(f"\n┌─ {title} {'─' * (50 - len(title) - 3)} ┐")
        
        for key, value in stats.items():
            # Format key
            formatted_key = key.replace('_', ' ').title()
            
            # Format value
            if isinstance(value, float):
                formatted_value = f"{value:.2f}"
            else:
                formatted_value = str(value)
            
            # Create line
            line = f"│ {formatted_key:<30} : {formatted_value:>15} │"
            output.append(line)
        
        output.append("└" + "─" * 53 + "┘")
        
        return "\n".join(output)
    
    @staticmethod
    def create_dashboard(project_metrics: Dict[str, Any], 
                        top_contributors: List[Dict[str, Any]],
                        title: str = "Performance Dashboard") -> str:
        """
        Create a comprehensive dashboard display.
        
        Args:
            project_metrics (Dict[str, Any]): Project metrics
            top_contributors (List[Dict[str, Any]]): Top contributors
            title (str): Dashboard title
            
        Returns:
            str: ASCII dashboard
        """
        output = []
        output.append(f"\n╔═══ {title} {'═' * (60 - len(title) - 6)} ╗")
        output.append("║" + " " * 64 + "║")
        
        # Key metrics
        output.append("║  📊 KEY METRICS:")
        output.append(f"║    • Total Contributors: {project_metrics.get('total_contributors', 0):<10}")
        output.append(f"║    • Total Contributions: {project_metrics.get('total_contributions', 0):<10}")
        output.append(f"║    • Completion Rate: {project_metrics.get('hacktoberfest_completion_rate', 0):.1f}%")
        output.append("║" + " " * 64 + "║")
        
        # Top contributor
        if top_contributors:
            top = top_contributors[0]
            output.append("║  ⭐ TOP CONTRIBUTOR:")
            output.append(f"║    • {top['name']} (@{top['username']})")
            output.append(f"║    • Contributions: {top['contributions']}")
        
        output.append("║" + " " * 64 + "║")
        output.append("╚" + "═" * 64 + "╝")
        
        return "\n".join(output)
    
    @staticmethod
    def create_contribution_types_pie(types_data: Dict[str, int], title: str = "") -> str:
        """
        Create a simple ASCII pie chart for contribution types.
        
        Args:
            types_data (Dict[str, int]): Contribution types and counts
            title (str): Chart title
            
        Returns:
            str: ASCII pie chart representation
        """
        output = []
        if title:
            output.append(f"\n{title}")
            output.append("=" * (len(title) + 10))
        
        total = sum(types_data.values())
        if total == 0:
            return "No data to display"
        
        pie_chars = ["⠀", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        
        for contrib_type, count in sorted(types_data.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100)
            pie_index = min(int(percentage / 12.5), 8)
            pie = pie_chars[pie_index]
            
            bar_width = int(percentage / 2)
            bar = "█" * bar_width
            
            output.append(f"{pie} {contrib_type:<20} │ {bar} {percentage:.1f}%")
        
        return "\n".join(output)


def print_metrics_visualization_examples():
    """Print example visualizations."""
    viz = MetricsVisualizer()
    
    # Example bar chart
    sample_data = {
        "Bug Fixes": 25,
        "Features": 18,
        "Documentation": 12,
        "Tests": 8
    }
    print(viz.create_bar_chart(sample_data, "Contribution Types"))
    
    # Example progress bar
    print("\n" + viz.create_progress_bar(4, 4, label="Hacktoberfest Progress"))
    
    # Example distribution
    distribution = {"0-1": 5, "2-3": 8, "4-5": 12, "6-10": 15, "11-20": 8, "21+": 2}
    print("\n" + viz.create_distribution_chart(distribution, "Contribution Distribution"))


if __name__ == "__main__":
    print_metrics_visualization_examples()
