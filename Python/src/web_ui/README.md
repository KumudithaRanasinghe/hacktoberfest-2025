# 🎃 Hacktoberfest 2025 Web UI

A modern, beautiful web interface for tracking Hacktoberfest contributions and contributors.

## Features

### 📊 Dashboard
- **Real-time Statistics**: View total contributors, contributions, repositories, and averages
- **Interactive Charts**: Visualize contribution types and top contributors
- **Recent Activity**: See the latest contributions across all contributors

### 👥 Contributors Management
- **Contributor Profiles**: View detailed information about each contributor
- **GitHub Integration**: Automatic avatar loading from GitHub profiles
- **Search & Filter**: Find contributors quickly
- **Activity Tracking**: See contribution history and statistics

### 🏆 Leaderboard
- **Top Contributors**: Celebrate the most active contributors
- **Podium Display**: Special recognition for top 3 contributors
- **Detailed Rankings**: Complete leaderboard with statistics

### ➕ Easy Data Entry
- **Add Contributors**: Simple form to register new contributors
- **Track Contributions**: Record contributions with detailed information
- **Form Validation**: Ensure data quality with client-side validation
- **Live Preview**: See how data will appear before submission

### 🎨 Modern Design
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Bootstrap 5**: Modern, clean interface
- **Dark Mode Support**: Automatic theme detection
- **Smooth Animations**: Enhanced user experience

## Quick Start

### 1. Install Dependencies
```bash
cd Python/
pip install -r requirements.txt
```

### 2. Launch Web UI
```bash
# Option 1: Using the main CLI
python src/main.py --web

# Option 2: Direct launch
python src/run_web_ui.py

# Option 3: Direct Flask app
cd src/web_ui/
python app.py
```

### 3. Open Your Browser
The web interface will automatically open at: `http://localhost:5000`

## API Endpoints

The web UI also provides REST API endpoints for integration:

- `GET /api/stats` - Project statistics
- `GET /api/contributors` - All contributors
- `GET /api/contributor/<username>` - Specific contributor details
- `GET /api/leaderboard` - Leaderboard data

## Screenshots

### Dashboard
![Dashboard showing project statistics and recent contributions]

### Contributors Page
![Grid view of all contributors with search and filter options]

### Leaderboard
![Top contributors with podium display and complete rankings]

### Add Contributor Form
![Form to add new contributors with live preview]

## Technical Details

### Tech Stack
- **Backend**: Flask (Python web framework)
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Forms**: Flask-WTF with validation
- **Data**: JSON file storage (same as CLI version)

### File Structure
```
src/web_ui/
├── app.py                 # Main Flask application
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # JavaScript functionality
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Dashboard page
    ├── contributors.html # Contributors listing
    ├── contributor_detail.html # Contributor profile
    ├── leaderboard.html  # Leaderboard page
    ├── add_contributor.html # Add contributor form
    └── add_contribution.html # Add contribution form
```

### Features in Detail

#### Dashboard Charts
- **Contribution Types**: Pie chart showing distribution of contribution types
- **Top Contributors**: Bar chart of most active contributors
- **Real-time Updates**: Statistics refresh automatically

#### Search & Filter
- **Live Search**: Instant search across contributor names and usernames
- **Sort Options**: Sort by name, contribution count, or recent activity
- **Filter by Type**: Filter contributions by type

#### Data Validation
- **Client-side**: Immediate feedback with JavaScript validation
- **Server-side**: Flask-WTF forms with validators
- **Error Handling**: Graceful error messages and recovery

## Customization

### Styling
Modify `static/css/style.css` to customize the appearance:
- Color scheme (using CSS custom properties)
- Layout and spacing
- Component styles

### Adding Features
The modular design makes it easy to add new features:
1. Add new routes in `app.py`
2. Create corresponding templates
3. Update navigation in `base.html`

### API Integration
The web UI can be used alongside other tools:
- All data is stored in the same JSON format as the CLI
- API endpoints allow external integrations
- CORS support for cross-origin requests

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python src/web_ui/app.py
```

### Making Changes
- Templates: Edit files in `templates/` directory
- Styles: Modify `static/css/style.css`
- JavaScript: Update `static/js/app.js`
- Backend: Modify `app.py` for new routes or functionality

## Production Deployment

For production deployment, consider:
- Using a production WSGI server (like Gunicorn)
- Setting up a reverse proxy (like Nginx)
- Securing the application with HTTPS
- Setting up database storage instead of JSON files

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --chdir src/web_ui app:app
```

## Contributing

The web UI is part of the larger Hacktoberfest 2025 project. Contributions are welcome:

1. **Bug Reports**: Open issues for any bugs you find
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Submit pull requests with your changes
4. **Documentation**: Help improve this documentation

## License

This project is part of the Hacktoberfest 2025 initiative and follows the same license as the main project.
