""" configuration """
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "webapp.db")
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "QWEWQYUhj342678gvmjhxckbdvkjbsabc"
REMEMBER_COOKIE_DURATION = timedelta(days=7)
COLORS = ["table-primary", "table-secondary", "table-info", "table-light", "table-success"]
RECOMMEND_ACTIONS = [f"Рецепт {n}" for n in range(1, 10)]
RATE_ACTIONS = [str(n) for n in range(1, 8)]
RECOMMEND_ACT = "action_"
RATE_ACT = "action"
