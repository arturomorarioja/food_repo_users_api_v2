"""
Food Repo users API
"""
__author__ = 'Arturo Mora-Rioja'
__date__ = 'October 2024'

import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from food_repo_users import food_repo_users, database

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_prefixed_env()

    database.init_app(app)

    app.register_blueprint(food_repo_users.bp)

    print(f'### FOOD REPO USERS API ###')
    print(f'Current environment: {os.getenv("ENVIRONMENT")}')
    print(f'Using database: {app.config.get("DATABASE")}')

    return app