"""A simple flask web app"""
import os
from flask import Flask
from flask import Blueprint, render_template, abort
from flask_wtf.csrf import CSRFProtect

import flask_login
from flask_bootstrap import Bootstrap5

from app.cli import create_database
from app.db import db
from app.logging_config import log_con
from app.simple_pages import simple_pages
from app.auth import auth
from app.db.models import User
from app.context_processors import utility_text_processors
from app.transactions import transactions

login_manager = flask_login.LoginManager()

def page_not_found(e):
    return render_template("404.html"), 404

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    if app.config["ENV"] == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif app.config["ENV"] == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif app.config["ENV"] == "testing":
        app.config.from_object("app.config.TestingConfig")

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    csrf = CSRFProtect(app)
    bootstrap = Bootstrap5(app)

    app.register_error_handler(404, page_not_found)

    app.register_blueprint(simple_pages)
    app.register_blueprint(auth)
    app.register_blueprint(transactions)
    app.register_blueprint(log_con)

    app.context_processor(utility_text_processors)
    # add command function to cli commands
    app.cli.add_command(create_database)

    # db_dir = "database/db.sqlite"
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # @app.route('/')
    # def hello():
    #     return 'Hello, World!'

    return app

@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None