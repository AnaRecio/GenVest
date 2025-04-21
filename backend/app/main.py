from flask import Flask
from flask_cors import CORS

# Import route blueprints
from app.routes.data import data_bp
from app.routes.report import report_bp
from app.routes.search import search_bp

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)

    # Enable Cross-Origin Resource Sharing (useful for frontend-backend communication)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register modular route blueprints
    app.register_blueprint(data_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(search_bp)

    return app

# Initialize the Flask app instance
app = create_app()
