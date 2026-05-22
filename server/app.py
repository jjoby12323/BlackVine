from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from .routes import events_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(events_bp)
    return app
