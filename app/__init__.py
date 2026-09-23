"""
SmartResume AI — Flask Application Factory
"""

import os
from flask import Flask
from config import Config
from app.models import Database


def create_app(config_class=Config):
    """Factory function to initialize and configure the Flask web application."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    app.config.from_object(config_class)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize SQLite Database schema
    Database.init_db()

    # Register blueprints / routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
