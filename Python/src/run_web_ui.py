#!/usr/bin/env python3
"""
Launcher script for the Hacktoberfest 2025 Web UI.
"""

import os
import sys
import webbrowser
from threading import Timer

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def open_browser():
    """Open the web browser after a short delay."""
    webbrowser.open('http://localhost:5000')

def main():
    """Main function to start the web UI."""
    print("🎃 Starting Hacktoberfest 2025 Web UI...")
    print("=" * 50)
    print("Web interface will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the Flask app
    try:
        from web_ui.app import app
        
        # Open browser after 1.5 seconds
        Timer(1.5, open_browser).start()
        
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except ImportError as e:
        print(f"Error importing Flask app: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🎃 Thank you for using Hacktoberfest 2025 Web UI!")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting the web UI: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
