"""
SmartResume AI — Application Entrypoint

Run this script to start the local development server:
python run.py
"""

from app import create_app
from config import Config

app = create_app(Config)

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("  SmartResume AI — Web Application Starting...")
    print("  Access the app in your browser at: http://127.0.0.1:5000")
    print("=" * 70 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=True)
