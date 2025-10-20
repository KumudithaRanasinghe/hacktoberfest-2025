import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import webbrowser
import os
from Contribute_Checker import ProjectTracker
from Contribute_Checker.metrics_visualizer import MetricsVisualizer

class HacktoberfestDesktopUI:
    def __init__(self):
        self.tracker = ProjectTracker()
        self.setup_window()
        self.create_menu()
        self.create_notebook()
        self.load_initial_data()

    def setup_window(self):
        self.root = tk.Tk()
        self.root.title("Hacktoberfest 2025 Tracker")
        self.root.geometry("900x600")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Helvetica", 16, "bold"))
        self.style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        self.style.configure("Stats.TLabel", font=("Helvetica", 10))
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Metrics", command=self.export_metrics)
        file_menu.add_command(label="Export to CSV", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Performance Report", command=self.show_performance_report)
        view_menu.add_command(label="Project Insights", command=self.show_insights)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=lambda: self.open_documentation())
        help_menu.add_command(label="About", command=self.show_about)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.contributors_tab = ttk.Frame(self.notebook)
        self.leaderboard_tab = ttk.Frame(self.notebook)
        self.add_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.contributors_tab, text="Contributors")
        self.notebook.add(self.leaderboard_tab, text="Leaderboard")
        self.notebook.add(self.add_tab, text="Add New")
        
        self.setup_dashboard()
        self.setup_contributors_view()
        self.setup_leaderboard()
        self.setup_add_forms()

    def setup_dashboard(self):
        # Title
        title = ttk.Label(
            self.dashboard_tab,
            text="Project Dashboard",
            style="Title.TLabel"
        )
        title.pack(pady=10)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(self.dashboard_tab, text="Project Statistics")
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        self.stats_labels = {
            'total_contributors': ttk.Label(stats_frame, style="Stats.TLabel"),
            'total_contributions': ttk.Label(stats_frame, style="Stats.TLabel"),
            'completion_rate': ttk.Label(stats_frame, style="Stats.TLabel"),
            'active_days': ttk.Label(stats_frame, style="Stats.TLabel")
        }
        
        for label in self.stats_labels.values():
            label.pack(anchor='w', padx=5, pady=2)
            
        # Recent Activity
        activity_frame = ttk.LabelFrame(self.dashboard_tab, text="Recent Activity")
        activity_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.activity_tree = ttk.Treeview(
            activity_frame,
            columns=("Date", "Username", "Action", "Details"),
            show="headings"
        )
        
        self.activity_tree.heading("Date", text="Date")
        self.activity_tree.heading("Username", text="Username")
        self.activity_tree.heading("Action", text="Action")
        self.activity_tree.heading("Details", text="Details")
        
        scrollbar = ttk.Scrollbar(
            activity_frame,
            orient="vertical",
            command=self.activity_tree.yview
        )
        self.activity_tree.configure(yscrollcommand=scrollbar.set)
        
        self.activity_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def setup_contributors_view(self):
        # Search frame
        search_frame = ttk.Frame(self.contributors_tab)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_contributors)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Contributors list
        self.contributors_tree = ttk.Treeview(
            self.contributors_tab,
            columns=("Username", "Name", "Email", "Contributions", "Status"),
            show="headings"
        )
        
        self.contributors_tree.heading("Username", text="Username")
        self.contributors_tree.heading("Name", text="Name")
        self.contributors_tree.heading("Email", text="Email")
        self.contributors_tree.heading("Contributions", text="Contributions")
        self.contributors_tree.heading("Status", text="Status")
        
        scrollbar = ttk.Scrollbar(
            self.contributors_tab,
            orient="vertical",
            command=self.contributors_tree.yview
        )
        self.contributors_tree.configure(yscrollcommand=scrollbar.set)
        
        self.contributors_tree.pack(side='left', fill='both', expand=True, padx=10, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        self.contributors_tree.bind('<Double-1>', self.show_contributor_details)

    def setup_leaderboard(self):
        # Title
        title = ttk.Label(
            self.leaderboard_tab,
            text="Engagement Leaderboard",
            style="Title.TLabel"
        )
        title.pack(pady=10)
        
        # Leaderboard table
        self.leaderboard_tree = ttk.Treeview(
            self.leaderboard_tab,
            columns=("Rank", "Username", "Score", "Streak", "Badges"),
            show="headings"
        )
        
        self.leaderboard_tree.heading("Rank", text="#")
        self.leaderboard_tree.heading("Username", text="Username")
        self.leaderboard_tree.heading("Score", text="Engagement Score")
        self.leaderboard_tree.heading("Streak", text="Streak")
        self.leaderboard_tree.heading("Badges", text="Badges")
        
        scrollbar = ttk.Scrollbar(
            self.leaderboard_tab,
            orient="vertical",
            command=self.leaderboard_tree.yview
        )
        self.leaderboard_tree.configure(yscrollcommand=scrollbar.set)
        
        self.leaderboard_tree.pack(side='left', fill='both', expand=True, padx=10, pady=5)
        scrollbar.pack(side='right', fill='y')

    def setup_add_forms(self):
        notebook = ttk.Notebook(self.add_tab)
        notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Add Contributor Form
        contributor_frame = ttk.Frame(notebook)
        notebook.add(contributor_frame, text="Add Contributor")
        
        ttk.Label(contributor_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(contributor_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(contributor_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(contributor_frame, textvariable=self.username_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(contributor_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(contributor_frame, textvariable=self.email_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(
            contributor_frame,
            text="Add Contributor",
            command=self.add_contributor
        ).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Add Contribution Form
        contribution_frame = ttk.Frame(notebook)
        notebook.add(contribution_frame, text="Add Contribution")
        
        ttk.Label(contribution_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.contrib_username_var = tk.StringVar()
        ttk.Entry(contribution_frame, textvariable=self.contrib_username_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(contribution_frame, text="Repository:").grid(row=1, column=0, padx=5, pady=5)
        self.repo_var = tk.StringVar()
        ttk.Entry(contribution_frame, textvariable=self.repo_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(contribution_frame, text="Type:").grid(row=2, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(
            contribution_frame,
            textvariable=self.type_var,
            values=["bug-fix", "feature", "documentation", "test", "other"]
        )
        type_combo.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(contribution_frame, text="Description:").grid(row=3, column=0, padx=5, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(contribution_frame, textvariable=self.description_var).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(contribution_frame, text="PR Number:").grid(row=4, column=0, padx=5, pady=5)
        self.pr_var = tk.StringVar()
        ttk.Entry(contribution_frame, textvariable=self.pr_var).grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Button(
            contribution_frame,
            text="Add Contribution",
            command=self.add_contribution
        ).grid(row=5, column=0, columnspan=2, pady=20)

    def load_initial_data(self):
        # Update dashboard statistics
        metrics = self.tracker.get_project_performance_metrics()
        self.update_dashboard_stats(metrics)
        
        # Load contributors
        self.refresh_contributors_list()
        
        # Update leaderboard
        self.refresh_leaderboard()

    def update_dashboard_stats(self, metrics):
        self.stats_labels['total_contributors'].config(
            text=f"Total Contributors: {metrics['total_contributors']}"
        )
        self.stats_labels['total_contributions'].config(
            text=f"Total Contributions: {metrics['total_contributions']}"
        )
        self.stats_labels['completion_rate'].config(
            text=f"Completion Rate: {metrics['hacktoberfest_completion_rate']:.1f}%"
        )
        self.stats_labels['active_days'].config(
            text=f"Active Days: {metrics['active_days']}"
        )

    def refresh_contributors_list(self):
        # Clear existing items
        for item in self.contributors_tree.get_children():
            self.contributors_tree.delete(item)
        
        # Add contributors
        for contributor in self.tracker.get_all_contributors():
            metrics = self.tracker.get_contributor_metrics(contributor.username)
            status = "✅" if metrics['hacktoberfest_complete'] else "🔄"
            
            self.contributors_tree.insert(
                "",
                "end",
                values=(
                    contributor.username,
                    contributor.name,
                    contributor.email,
                    metrics['total_contributions'],
                    status
                )
            )

    def refresh_leaderboard(self):
        # Clear existing items
        for item in self.leaderboard_tree.get_children():
            self.leaderboard_tree.delete(item)
        
        # Get rankings
        rankings = self.tracker.get_contributors_ranking()
        
        for rank in rankings:
            metrics = self.tracker.get_contributor_metrics(rank['username'])
            badges = "🏆" if metrics['hacktoberfest_complete'] else ""
            if metrics['contribution_streak'] >= 3:
                badges += "🔥"
            
            self.leaderboard_tree.insert(
                "",
                "end",
                values=(
                    rank['rank'],
                    rank['username'],
                    f"{rank['engagement_score']:.1f}",
                    f"{metrics['contribution_streak']} days",
                    badges
                )
            )

    def filter_contributors(self, *args):
        search_text = self.search_var.get().lower()
        
        for item in self.contributors_tree.get_children():
            values = self.contributors_tree.item(item)['values']
            if (search_text in str(values[0]).lower() or  # username
                search_text in str(values[1]).lower() or  # name
                search_text in str(values[2]).lower()):   # email
                self.contributors_tree.reattach(item, "", "end")
            else:
                self.contributors_tree.detach(item)

    def add_contributor(self):
        name = self.name_var.get().strip()
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        
        if not all([name, username, email]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            contributor = self.tracker.add_contributor(name, username, email)
            messagebox.showinfo("Success", f"Added contributor: {contributor.name}")
            
            # Clear form
            self.name_var.set("")
            self.username_var.set("")
            self.email_var.set("")
            
            # Refresh views
            self.refresh_contributors_list()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_contribution(self):
        username = self.contrib_username_var.get().strip()
        repo = self.repo_var.get().strip()
        contrib_type = self.type_var.get()
        description = self.description_var.get().strip()
        pr_number = self.pr_var.get().strip()
        
        if not all([username, repo, contrib_type, description]):
            messagebox.showerror("Error", "Required fields are missing")
            return
        
        try:
            success = self.tracker.add_contribution(
                username, repo, contrib_type, description,
                pr_number if pr_number else None
            )
            
            if success:
                messagebox.showinfo("Success", "Contribution added successfully")
                
                # Clear form
                self.contrib_username_var.set("")
                self.repo_var.set("")
                self.type_var.set("")
                self.description_var.set("")
                self.pr_var.set("")
                
                # Refresh views
                self.refresh_contributors_list()
                self.refresh_leaderboard()
                
            else:
                messagebox.showerror("Error", "Failed to add contribution")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_contributor_details(self, event):
        item = self.contributors_tree.selection()[0]
        username = self.contributors_tree.item(item)['values'][0]
        
        # Create detail window
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Contributor Details - {username}")
        detail_window.geometry("500x400")
        
        # Get metrics
        metrics = self.tracker.get_contributor_metrics(username)
        contributor = self.tracker.get_contributor(username)
        
        # Display information
        ttk.Label(
            detail_window,
            text=f"{contributor.name} (@{username})",
            style="Title.TLabel"
        ).pack(pady=10)
        
        details_frame = ttk.Frame(detail_window)
        details_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        details = [
            ("Email", contributor.email),
            ("Total Contributions", metrics['total_contributions']),
            ("Contribution Streak", f"{metrics['contribution_streak']} days"),
            ("Days Active", metrics['days_active']),
            ("Average Days Between Contributions", f"{metrics['average_days_between_contributions']:.1f}"),
            ("Hacktoberfest Complete", "Yes ✅" if metrics['hacktoberfest_complete'] else "No ❌"),
            ("Most Active Day", metrics['most_active_day'] or "N/A")
        ]
        
        for i, (label, value) in enumerate(details):
            ttk.Label(details_frame, text=f"{label}:", style="Header.TLabel").grid(
                row=i, column=0, sticky='w', padx=5, pady=2
            )
            ttk.Label(details_frame, text=str(value)).grid(
                row=i, column=1, sticky='w', padx=5, pady=2
            )

    def export_metrics(self):
        try:
            self.tracker.export_metrics("metrics_export.json")
            messagebox.showinfo(
                "Success",
                "Metrics exported to metrics_export.json"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_csv(self):
        try:
            self.tracker.export_csv("all")
            messagebox.showinfo(
                "Success",
                "Data exported to CSV files in the exports directory"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_performance_report(self):
        metrics = self.tracker.get_project_performance_metrics()
        report_window = tk.Toplevel(self.root)
        report_window.title("Performance Report")
        report_window.geometry("600x400")
        
        text_widget = tk.Text(report_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill='both', expand=True)
        
        report = f"""Performance Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
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
        
        text_widget.insert('1.0', report)
        text_widget.config(state='disabled')

    def show_insights(self):
        insights = self.tracker.get_performance_insights()
        
        insights_window = tk.Toplevel(self.root)
        insights_window.title("Project Insights")
        insights_window.geometry("600x400")
        
        text_widget = tk.Text(insights_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill='both', expand=True)
        
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
        
        text_widget.config(state='disabled')

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Hacktoberfest 2025 Project Tracker\n\n"
            "A tool for tracking and managing Hacktoberfest contributions.\n\n"
            "Version: 1.0.0\n"
            "Created by: Hacktoberfest Contributors"
        )

    def open_documentation(self):
        docs_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "docs",
            "API.md"
        )
        if os.path.exists(docs_path):
            webbrowser.open(f"file://{docs_path}")
        else:
            messagebox.showerror(
                "Error",
                "Documentation file not found"
            )

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HacktoberfestDesktopUI()
    app.run()