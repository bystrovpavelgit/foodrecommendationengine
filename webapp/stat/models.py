"""models for SQLite"""
from webapp.db import DB


class Recipe(DB.Model):
    """ Recipes table """
    __tablename__ = "recipe"
    id = DB.Column(DB.Integer, primary_key=True)
