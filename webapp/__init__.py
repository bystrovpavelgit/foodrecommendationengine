"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    Flask web-app for recipe recommendation
"""
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug import exceptions
from webapp.db import DB
from webapp.user.models import User
from webapp.calculate.views import blueprint as calc_blueprint
from webapp.user.views import blueprint as user_blueprint
from webapp.stat.views import blueprint as stat_blueprint
from webapp.recommend.views import blueprint as recommend_blueprint


class InsufficientStorage(exceptions.HTTPException):
    code = 507
    description = 'Not enough storage space.'


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
    app.register_blueprint(calc_blueprint)

    migrate = Migrate(app, DB)

    @app.errorhandler(exceptions.BadRequest)
    def handle_bad_request(err):
        return 'bad request!', 400

    @app.errorhandler(InsufficientStorage)
    def handle_507(err):
        return 'Not enough storage space', 507

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(user_id)
        return user

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
