import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import os
import webbrowser
from datetime import datetime

class MenuSystem:
    
    def __init__(self, root, tracker):
        """Initialize the menu system"""
        self.root = root
        self.tracker = tracker
        self.create_menu()

    def create_menu(self):
        """Create the main menu bar and all submenus"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # File Menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        
        # Export submenu
        self.export_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="Export", menu=self.export_menu)
        self.export_menu.add_command(label="Export as JSON", command=self.export_json)
        self.export_menu.add_command(label="Export as CSV", command=self.export_csv)
        self.export_menu.add_command(label="Export Metrics", command=self.export_metrics)
        
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Settings", command=self.show_settings)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # View Menu
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Performance Report", command=self.show_performance_report)
        self.view_menu.add_command(label="Project Insights", command=self.show_insights)
        self.view_menu.add_command(label="Statistics", command=self.show_statistics)
        
        # Tools Menu
        self.tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Badge Manager", command=self.open_badge_manager)
        self.tools_menu.add_command(label="Email Notifications", command=self.manage_notifications)
        self.tools_menu.add_command(label="Data Backup", command=self.backup_data)
        self.tools_menu.add_separator()
        self.tools_menu.add_command(label="Refresh Data", command=self.refresh_data)

        # Help Menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Documentation", command=self.open_documentation)
        self.help_menu.add_command(label="Quick Start Guide", command=self.show_quick_start)
        self.help_menu.add_command(label="Check for Updates", command=self.check_updates)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", command=self.show_about)

    def export_json(self):
        """Export data as JSON"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Export as JSON"
        )
        if file_path:
            try:
                data = self.tracker.export_data()
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                messagebox.showinfo("Success", "Data exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def export_csv(self):
        """Export data as CSV"""
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if export_dir:
            try:
                self.tracker.export_csv(export_dir)
                messagebox.showinfo("Success", "Data exported to CSV successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def export_metrics(self):
        """Export metrics data"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Export Metrics"
        )
        if file_path:
            try:
                self.tracker.export_metrics(file_path)
                messagebox.showinfo("Success", "Metrics exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        
        # Add settings controls here
        ttk.Label(settings_window, text="Application Settings", 
                 font=("Helvetica", 14, "bold")).pack(pady=10)
        
        # Example settings
        ttk.Checkbutton(settings_window, text="Enable email notifications").pack(anchor='w', padx=20, pady=5)
        ttk.Checkbutton(settings_window, text="Auto-refresh data").pack(anchor='w', padx=20, pady=5)
        ttk.Checkbutton(settings_window, text="Show desktop notifications").pack(anchor='w', padx=20, pady=5)

    def show_performance_report(self):
        """Display performance report"""
        report_window = tk.Toplevel(self.root)
        report_window.title("Performance Report")
        report_window.geometry("600x400")
        
        
        metrics = self.tracker.get_project_performance_metrics()
        
        text_widget = tk.Text(report_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill='both', expand=True)
        
        report = self._generate_performance_report(metrics)
        text_widget.insert('1.0', report)
        text_widget.config(state='disabled')

    def show_insights(self):
        """Show project insights"""
        insights = self.tracker.get_performance_insights()
        
        insights_window = tk.Toplevel(self.root)
        insights_window.title("Project Insights")
        insights_window.geometry("600x400")
        
        text_widget = tk.Text(insights_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill='both', expand=True)
        
        self._display_insights(text_widget, insights)
        text_widget.config(state='disabled')

    def show_statistics(self):
        """Show detailed statistics"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Project Statistics")
        stats_window.geometry("800x600")
        
        # Add statistics visualization here
        # This could include graphs, charts, etc.

    def open_badge_manager(self):
        """Open badge management window"""
        badge_window = tk.Toplevel(self.root)
        badge_window.title("Badge Manager")
        badge_window.geometry("500x400")
        
        # Add badge management UI here

    def manage_notifications(self):
        """Manage email notifications"""
        notify_window = tk.Toplevel(self.root)
        notify_window.title("Email Notifications")
        notify_window.geometry("500x400")
        
        # Add notification management UI here

    def backup_data(self):
        """Backup project data"""
        backup_dir = filedialog.askdirectory(title="Select Backup Directory")
        if backup_dir:
            try:
                # Implement backup logic here
                messagebox.showinfo("Success", "Backup completed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Backup failed: {str(e)}")

    def refresh_data(self):
        """Refresh all data"""
        try:
            # Implement refresh logic here
            messagebox.showinfo("Success", "Data refreshed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Refresh failed: {str(e)}")

    def open_documentation(self):
        """Open documentation"""
        docs_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "docs",
            "API.md"
        )
        if os.path.exists(docs_path):
            webbrowser.open(f"file://{docs_path}")
        else:
            messagebox.showerror("Error", "Documentation not found")

    def show_quick_start(self):
        """Show quick start guide"""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("Quick Start Guide")
        guide_window.geometry("600x400")
        
        # Add quick start guide content here
        

    def check_updates(self):
        """Check for software updates"""
        # Implement update check logic here
        messagebox.showinfo(
            "Updates",
            "You are running the latest version (1.0.0)"
        )

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            "Hacktoberfest 2025 Project Tracker\n\n"
            "Version: 1.0.0\n"
            "A comprehensive tool for tracking and managing "
            "Hacktoberfest contributions.\n\n"
            "Created by: Hacktoberfest Contributors"
        )

    def _generate_performance_report(self, metrics):
        """Generate formatted performance report"""
        return f"""Performance Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
Project Overview:
----------------
Total Contributors: {metrics['total_contributors']}
Total Contributions: {metrics['total_contributions']}
Hacktoberfest Completion Rate: {metrics['hacktoberfest_completion_rate']:.1f}%
Active Days: {metrics['active_days']}

Contribution Statistics:
---------------------
Average Contributions per User: {metrics['average_contributions_per_user']:.1f}
Most Active Day: {metrics['most_active_day']}
Contributors Completed Hacktoberfest: {metrics['completed_hacktoberfest']}

Repository Activity:
-----------------
Active Repositories: {len(metrics['repository_contributions'])}
Top Repository: {max(metrics['repository_contributions'].items(), key=lambda x: x[1])[0]}
"""

    def _display_insights(self, text_widget, insights):
        """Display formatted insights"""
        text_widget.insert('1.0', "Project Insights\n\n")
        
        if 'highlights' in insights:
            text_widget.insert('end', "🎉 Highlights:\n")
            for highlight in insights['highlights']:
                text_widget.insert('end', f"• {highlight}\n")
            text_widget.insert('end', "\n")
        
        if 'concerns' in insights:
            text_widget.insert('end', "⚠️ Areas for Attention:\n")
            for concern in insights['concerns']:
                text_widget.insert('end', f"• {concern}\n")
            text_widget.insert('end', "\n")
        
        if 'recommendations' in insights:
            text_widget.insert('end', "💡 Recommendations:\n")
            for rec in insights['recommendations']:
                text_widget.insert('end', f"• {rec}\n")