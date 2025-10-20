#!/usr/bin/env python3
"""
Flask web application for the Hacktoberfest 2025 Project Tracker.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Optional
from flask_cors import CORS

# Add the parent directory to the path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Contribute_Checker import ProjectTracker, Contributor
from Contribute_Checker.notification_system import notification_manager, NotificationType, NotificationPriority

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hacktoberfest-2025-secret-key'
CORS(app)

# Initialize the project tracker
tracker = ProjectTracker("Hacktoberfest 2025 Web UI")

# Template helper functions
@app.template_filter('get_type_color')
def get_type_color(contribution_type):
    """Get Bootstrap color class for contribution type."""
    colors = {
        'bug-fix': 'danger',
        'feature': 'success',
        'documentation': 'info',
        'testing': 'warning',
        'refactoring': 'purple',
        'enhancement': 'orange'
    }
    return colors.get(contribution_type, 'secondary')

@app.context_processor
def inject_helpers():
    """Inject helper functions into all templates."""
    return {
        'get_type_color': get_type_color,
        'notification_count': lambda username=None: len(notification_manager.get_user_notifications(username or 'anonymous', unread_only=True)) if username else 0
    }


class ContributorForm(FlaskForm):
    """Form for adding new contributors."""
    name = StringField('Full Name', validators=[DataRequired()])
    github_username = StringField('GitHub Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), Optional()])
    submit = SubmitField('Add Contributor')


class ContributionForm(FlaskForm):
    """Form for adding new contributions."""
    github_username = SelectField('Contributor', validators=[DataRequired()])
    repo_name = StringField('Repository Name', validators=[DataRequired()])
    contribution_type = SelectField('Contribution Type', 
                                  choices=[
                                      ('bug-fix', 'Bug Fix'),
                                      ('feature', 'Feature'),
                                      ('documentation', 'Documentation'),
                                      ('testing', 'Testing'),
                                      ('refactoring', 'Refactoring'),
                                      ('enhancement', 'Enhancement')
                                  ],
                                  validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    pr_number = IntegerField('Pull Request Number', validators=[Optional()])
    submit = SubmitField('Add Contribution')


@app.route('/')
def index():
    """Home page showing project overview."""
    stats = tracker.get_project_stats()
    recent_contributions = tracker.get_recent_contributions(limit=10)
    return render_template('index.html', stats=stats, recent_contributions=recent_contributions)


@app.route('/contributors')
def contributors():
    """Page showing all contributors."""
    all_contributors = tracker.get_all_contributors()
    return render_template('contributors.html', contributors=all_contributors)


@app.route('/contributor/<username>')
def contributor_detail(username):
    """Page showing detailed information about a specific contributor."""
    contributor = tracker.get_contributor(username)
    if not contributor:
        flash(f'Contributor {username} not found!', 'error')
        return redirect(url_for('contributors'))
    return render_template('contributor_detail.html', contributor=contributor)


@app.route('/leaderboard')
def leaderboard():
    """Page showing the contribution leaderboard."""
    leaderboard_data = tracker.get_leaderboard()
    return render_template('leaderboard.html', leaderboard=leaderboard_data)


@app.route('/add-contributor', methods=['GET', 'POST'])
def add_contributor():
    """Page for adding new contributors."""
    form = ContributorForm()
    
    if form.validate_on_submit():
        try:
            contributor = tracker.add_contributor(
                form.name.data,
                form.github_username.data,
                form.email.data
            )
            flash(f'Successfully added contributor: {contributor.name}', 'success')
            return redirect(url_for('contributors'))
        except Exception as e:
            flash(f'Error adding contributor: {str(e)}', 'error')
        else:
            # Create welcome notification
            notification_manager.create_welcome_notification(
                contributor.github_username, 
                contributor.name
            )
    
    return render_template('add_contributor.html', form=form)


@app.route('/add-contribution', methods=['GET', 'POST'])
def add_contribution():
    """Page for adding new contributions."""
    form = ContributionForm()
    
    # Populate the contributor choices
    all_contributors = tracker.get_all_contributors()
    form.github_username.choices = [
        (contrib.github_username, f"{contrib.name} (@{contrib.github_username})")
        for contrib in all_contributors
    ]
    
    if form.validate_on_submit():
        try:
            success = tracker.add_contribution(
                form.github_username.data,
                form.repo_name.data,
                form.contribution_type.data,
                form.description.data,
                form.pr_number.data
            )
            if success:
                flash('Successfully added contribution!', 'success')
                
                # Check for milestone achievements
                contributor = tracker.get_contributor(form.github_username.data)
                if contributor:
                    contribution_count = contributor.get_contribution_count()
                    is_complete = contribution_count >= 4
                    
                    # Create milestone notification
                    notification_manager.create_milestone_notification(
                        form.github_username.data,
                        contribution_count,
                        is_complete
                    )
                
                return redirect(url_for('index'))
            else:
                flash('Failed to add contribution. Contributor not found.', 'error')
        except Exception as e:
            flash(f'Error adding contribution: {str(e)}', 'error')
    
    return render_template('add_contribution.html', form=form)


@app.route('/api/stats')
def api_stats():
    """API endpoint for project statistics."""
    return jsonify(tracker.get_project_stats())


@app.route('/api/contributors')
def api_contributors():
    """API endpoint for all contributors."""
    contributors = tracker.get_all_contributors()
    return jsonify([{
        'name': c.name,
        'github_username': c.github_username,
        'email': c.email,
        'contribution_count': c.get_contribution_count(),
        'joined_date': c.joined_date.isoformat()
    } for c in contributors])


@app.route('/api/contributor/<username>')
def api_contributor(username):
    """API endpoint for specific contributor details."""
    contributor = tracker.get_contributor(username)
    if not contributor:
        return jsonify({'error': 'Contributor not found'}), 404
    
    return jsonify({
        'name': contributor.name,
        'github_username': contributor.github_username,
        'email': contributor.email,
        'contribution_count': contributor.get_contribution_count(),
        'joined_date': contributor.joined_date.isoformat(),
        'contributions': contributor.contributions
    })


@app.route('/api/leaderboard')
def api_leaderboard():
    """API endpoint for leaderboard data."""
    return jsonify(tracker.get_leaderboard())


@app.route('/notifications')
def notifications():
    """Page showing user notifications."""
    # For demo purposes, we'll use 'anonymous' user
    # In a real app, you'd get this from user session/auth
    username = request.args.get('user', 'anonymous')
    
    user_notifications = notification_manager.get_user_notifications(username)
    stats = notification_manager.get_notification_stats(username)
    
    return render_template('notifications.html', 
                         notifications=user_notifications, 
                         stats=stats,
                         username=username)


@app.route('/api/notifications')
def api_notifications():
    """API endpoint for user notifications."""
    username = request.args.get('user', 'anonymous')
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    limit = request.args.get('limit', type=int)
    
    user_notifications = notification_manager.get_user_notifications(
        username, unread_only=unread_only, limit=limit
    )
    
    return jsonify([notification.to_dict() for notification in user_notifications])


@app.route('/api/notifications/stats')
def api_notification_stats():
    """API endpoint for notification statistics."""
    username = request.args.get('user', 'anonymous')
    stats = notification_manager.get_notification_stats(username)
    return jsonify(stats)


@app.route('/api/notifications/<notification_id>/read', methods=['POST'])
def api_mark_notification_read(notification_id):
    """API endpoint to mark a notification as read."""
    success = notification_manager.mark_as_read(notification_id)
    return jsonify({'success': success})


@app.route('/api/notifications/<notification_id>/dismiss', methods=['POST'])
def api_dismiss_notification(notification_id):
    """API endpoint to dismiss a notification."""
    success = notification_manager.mark_as_dismissed(notification_id)
    return jsonify({'success': success})


@app.route('/api/notifications/mark-all-read', methods=['POST'])
def api_mark_all_read():
    """API endpoint to mark all notifications as read for a user."""
    username = request.args.get('user', 'anonymous')
    
    user_notifications = notification_manager.get_user_notifications(username)
    count = 0
    
    for notification in user_notifications:
        if not notification.read:
            notification_manager.mark_as_read(notification.id)
            count += 1
    
    return jsonify({'success': True, 'count': count})


@app.route('/api/notifications/clear-all', methods=['POST'])
def api_clear_all_notifications():
    """API endpoint to clear all notifications for a user."""
    username = request.args.get('user', 'anonymous')
    
    user_notifications = notification_manager.get_user_notifications(username)
    count = 0
    
    for notification in user_notifications:
        notification_manager.mark_as_dismissed(notification.id)
        count += 1
    
    return jsonify({'success': True, 'count': count})


@app.route('/api/notifications/create', methods=['POST'])
def api_create_notification():
    """API endpoint to create a new notification."""
    data = request.get_json()
    
    try:
        notification_type = NotificationType(data.get('type', 'info'))
        priority = NotificationPriority(data.get('priority', 'normal'))
        
        notification_id = notification_manager.create_notification(
            title=data['title'],
            message=data['message'],
            notification_type=notification_type,
            priority=priority,
            username=data.get('username'),
            expires_in_hours=data.get('expires_in_hours', 24),
            action_url=data.get('action_url'),
            action_text=data.get('action_text'),
            metadata=data.get('metadata')
        )
        
        return jsonify({'success': True, 'notification_id': notification_id})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/notifications/system', methods=['POST'])
def api_create_system_notification():
    """API endpoint to create a system-wide notification."""
    data = request.get_json()
    
    try:
        priority = NotificationPriority(data.get('priority', 'normal'))
        
        notification_id = notification_manager.create_system_notification(
            title=data['title'],
            message=data['message'],
            priority=priority,
            expires_in_hours=data.get('expires_in_hours', 48)
        )
        
        return jsonify({'success': True, 'notification_id': notification_id})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/achievement-badges')
def achievement_badges():
    """Display the achievement badges page."""
    return render_template('achievement_badges.html')


@app.route('/api/badges')
def api_badges():
    """API endpoint to get all achievement badges data."""
    # In a real implementation, this would fetch from a database
    badges_data = {
        'earned': [
            {
                'id': 'first-contribution',
                'name': 'First Contribution',
                'description': 'Made your first contribution to Hacktoberfest!',
                'icon': 'fas fa-seedling',
                'category': 'contribution',
                'earned_date': '2024-10-02'
            },
            {
                'id': 'streak-master',
                'name': 'Streak Master',
                'description': 'Maintained a 5-day contribution streak!',
                'icon': 'fas fa-fire',
                'category': 'contribution',
                'earned_date': '2024-10-07'
            },
            {
                'id': 'bug-hunter',
                'name': 'Bug Hunter',
                'description': 'Found and fixed 3 bugs in different projects!',
                'icon': 'fas fa-bug',
                'category': 'contribution',
                'earned_date': '2024-10-12'
            }
        ],
        'in_progress': [
            {
                'id': 'feature-creator',
                'name': 'Feature Creator',
                'description': 'Implement 5 new features across projects',
                'icon': 'fas fa-plus-circle',
                'category': 'contribution',
                'progress': {'current': 2, 'total': 5}
            },
            {
                'id': 'documentation-guru',
                'name': 'Documentation Guru',
                'description': 'Improve documentation in 10 repositories',
                'icon': 'fas fa-book',
                'category': 'contribution',
                'progress': {'current': 1, 'total': 10}
            },
            {
                'id': 'team-player',
                'name': 'Team Player',
                'description': 'Collaborate on 3 different team projects',
                'icon': 'fas fa-handshake',
                'category': 'engagement',
                'progress': {'current': 1, 'total': 3}
            },
            {
                'id': 'milestone-achiever',
                'name': 'Milestone Achiever',
                'description': 'Complete all 4 required Hacktoberfest PRs',
                'icon': 'fas fa-flag-checkered',
                'category': 'special',
                'progress': {'current': 3, 'total': 4}
            },
            {
                'id': 'super-contributor',
                'name': 'Super Contributor',
                'description': 'Make 20+ contributions in one month',
                'icon': 'fas fa-rocket',
                'category': 'contribution',
                'progress': {'current': 5, 'total': 20}
            },
            {
                'id': 'hacktoberfest-hero',
                'name': 'Hacktoberfest Hero',
                'description': 'Complete Hacktoberfest and earn 10+ badges',
                'icon': 'fas fa-crown',
                'category': 'special',
                'progress': {'current': 3, 'total': 10}
            }
        ],
        'locked': [
            {
                'id': 'test-champion',
                'name': 'Test Champion',
                'description': 'Add comprehensive tests to 5 projects',
                'icon': 'fas fa-vial',
                'category': 'contribution',
                'progress': {'current': 0, 'total': 5}
            },
            {
                'id': 'early-bird',
                'name': 'Early Bird',
                'description': 'Start contributing in the first week of October',
                'icon': 'fas fa-sun',
                'category': 'special',
                'status': 'missed'
            },
            {
                'id': 'mentor',
                'name': 'Mentor',
                'description': 'Help 5 new contributors with their first PRs',
                'icon': 'fas fa-chalkboard-teacher',
                'category': 'engagement',
                'progress': {'current': 0, 'total': 5}
            }
        ]
    }
    
    return jsonify(badges_data)


@app.route('/api/badges/earn/<badge_id>', methods=['POST'])
def api_earn_badge(badge_id):
    """API endpoint to earn a badge (for testing/simulation)."""
    # In a real implementation, this would validate the achievement
    # and update the database
    
    # Create a notification for the earned badge
    try:
        notification_manager.create_notification(
            title=f"🎉 Badge Earned!",
            message=f"Congratulations! You've earned the {badge_id.replace('-', ' ').title()} badge!",
            notification_type=NotificationType.ACHIEVEMENT,
            priority=NotificationPriority.HIGH,
            username=request.args.get('username', 'anonymous'),
            action_url=url_for('achievement_badges'),
            action_text='View Badge'
        )
        
        return jsonify({'success': True, 'message': f'Badge {badge_id} earned!'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/git/pull', methods=['POST'])
def api_git_pull():
    """API endpoint to perform git pull and return timing information."""
    import subprocess
    import time
    import os
    
    try:
        # Get the repository root directory
        repo_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Record start time
        start_time = time.time()
        
        # Perform git pull
        result = subprocess.run(
            ['git', 'pull'],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )
        
        # Record end time
        end_time = time.time()
        duration_ms = int((end_time - start_time) * 1000)
        
        if result.returncode == 0:
            # Parse git output to count changes
            output = result.stdout.strip()
            changes = 0
            
            # Simple parsing for common git pull outputs
            if "files changed" in output:
                import re
                match = re.search(r'(\d+) files? changed', output)
                if match:
                    changes = int(match.group(1))
            elif "Already up to date" in output or "Already up-to-date" in output:
                changes = 0
            elif output and "Updating" in output:
                # Estimate changes from output lines
                changes = len([line for line in output.split('\n') if line.strip() and not line.startswith('From')])
            
            # Create a notification for successful pull
            notification_manager.create_notification(
                title="📥 Git Pull Completed",
                message=f"Repository updated successfully in {duration_ms}ms. {changes} files changed.",
                notification_type=NotificationType.SUCCESS,
                priority=NotificationPriority.LOW,
                username='system',
                expires_in_hours=2
            )
            
            return jsonify({
                'success': True,
                'duration': duration_ms,
                'changes': changes,
                'message': output if output else 'Repository is up to date',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            # Git pull failed
            error_message = result.stderr.strip() or result.stdout.strip() or 'Unknown git error'
            
            # Create a notification for failed pull
            notification_manager.create_notification(
                title="❌ Git Pull Failed",
                message=f"Failed to update repository: {error_message}",
                notification_type=NotificationType.ERROR,
                priority=NotificationPriority.HIGH,
                username='system',
                expires_in_hours=6
            )
            
            return jsonify({
                'success': False,
                'error': error_message,
                'duration': duration_ms
            }), 400
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Git pull timed out after 60 seconds',
            'duration': 60000
        }), 408
        
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'Git command not found. Please ensure Git is installed.',
            'duration': 0
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'duration': 0
        }), 500


@app.route('/api/git/status')
def api_git_status():
    """API endpoint to get git repository status."""
    import subprocess
    import os
    
    try:
        repo_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Get git status
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            changes = len([line for line in result.stdout.strip().split('\n') if line.strip()])
            
            # Get last commit info
            commit_result = subprocess.run(
                ['git', 'log', '-1', '--format=%H|%s|%an|%ar'],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            commit_info = {}
            if commit_result.returncode == 0 and commit_result.stdout.strip():
                parts = commit_result.stdout.strip().split('|')
                if len(parts) >= 4:
                    commit_info = {
                        'hash': parts[0][:8],
                        'message': parts[1],
                        'author': parts[2],
                        'time': parts[3]
                    }
            
            return jsonify({
                'success': True,
                'uncommitted_changes': changes,
                'clean': changes == 0,
                'last_commit': commit_info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to get git status'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
