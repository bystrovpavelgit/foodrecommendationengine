"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    Flask web-app for recipe recommendation
"""
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.db import DB
from webapp.user.models import User
from webapp.stat.models import Recipe
from webapp.user.views import blueprint as user_blueprint
from webapp.stat.views import blueprint as stat_blueprint
from webapp.recommend.views import blueprint as recommend_blueprint


def create_app():
    """ main app for recipe recommendation """
    app = Flask(__name__, static_url_path="/", static_folder="/")
    app.config.from_pyfile("config.py")
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    DB.init_app(app)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(stat_blueprint)
    app.register_blueprint(recommend_blueprint)

    migrate = Migrate(app, DB)

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(user_id)
        return user

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
