"""models for SQLite"""
from webapp.db import DB

class Recipe(DB.Model):
    """ Recipes table """
    __tablename__ = "recipe"
    id = DB.Column(DB.Integer, primary_key=True)


class Note(DB.Model):
    """ Note table """
    __tablename__ = "note"
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(300))
    pic_url = DB.Column(DB.String(300))
    pic = DB.Column(DB.String(100))
    ingredients = DB.Column(DB.String(2000))
    mera = DB.Column(DB.String(2000))
    directions = DB.Column(DB.String(2000))
    cusine = DB.Column(DB.String(100))
    typed = DB.Column(DB.String(100))
    url = DB.Column(DB.String(300))

    def __repr__(self):
        """repr method"""
        return f"<Note {self.id} {self.url}>"
