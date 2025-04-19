from flask import Flask
from flask_cors import CORS

# Import blueprints
from app.routes.data import data_bp
from app.routes.report import report_bp
from app.routes.search import search_bp  

from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app) 


    app.register_blueprint(data_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(search_bp)  

    return app

app = create_app()
