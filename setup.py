"""Setup configuration for the Hacktoberfest 2025 project."""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    """Read README.md file for long description."""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "A simple Python project for tracking Hacktoberfest contributions."

# Read requirements
def read_requirements():
    """Read requirements.txt file."""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    requirements = []
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            requirements = [
                line.strip() 
                for line in f.readlines() 
                if line.strip() and not line.startswith("#") and not line.startswith("python")
            ]
    return requirements

setup(
    name="hacktoberfest-2025",
    version="1.0.0",
    author="Hacktoberfest Contributors",
    author_email="contributors@hacktoberfest.com",
    description="A simple Python project for tracking Hacktoberfest 2025 contributions",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/IEEE-Student-Branch-NSBM/hacktoberfest-2025",
    project_urls={
        "Bug Tracker": "https://github.com/IEEE-Student-Branch-NSBM/hacktoberfest-2025/issues",
        "Documentation": "https://github.com/IEEE-Student-Branch-NSBM/hacktoberfest-2025#readme",
        "Source Code": "https://github.com/IEEE-Student-Branch-NSBM/hacktoberfest-2025",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
        "cli": [
            "colorama>=0.4.6",
            "rich>=13.0.0",
            "click>=8.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "hacktoberfest=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="hacktoberfest, open-source, contributions, tracking, python",
)