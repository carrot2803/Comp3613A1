from flask import Flask
from flask_cors import CORS
from App.database import init_db
from App.config import load_config


def create_app(overrides={}) -> Flask:
    app = Flask(__name__, static_url_path="/static")
    load_config(app, overrides)
    CORS(app)
    init_db(app)
    app.app_context().push()
    return app
