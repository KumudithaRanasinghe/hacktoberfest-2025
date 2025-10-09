"""
Hacktoberfest 2025 Project
A simple Python application for tracking Hacktoberfest contributions.
"""

__version__ = "1.0.0"
__author__ = "Hacktoberfest Contributors"
__email__ = "contributors@hacktoberfest.com"

from .contributor import Contributor
from .project_tracker import ProjectTracker

__all__ = ["Contributor", "ProjectTracker"]