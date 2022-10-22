""" Flask app """
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.db import DB
from webapp.user.models import User
from webapp.stat.models import Recipe
from webapp.user.views import blueprint as user_blueprint
from webapp.stat.views import blueprint as stat_blueprint


def create_app():
    """ starting app for Flask object detection site """
    app = Flask(__name__, static_url_path="/static/", static_folder="/static/")
    app.config.from_pyfile("config.py")
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    DB.init_app(app)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(stat_blueprint)
    migrate = Migrate(app, DB)

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(user_id)
        return user

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
