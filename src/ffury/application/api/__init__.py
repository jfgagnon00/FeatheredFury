from flask import Flask
from .routes import api_routes

def create_api():
    api = Flask(__name__)
    api.register_blueprint(api_routes)
    return api
