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
        'get_type_color': get_type_color
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
