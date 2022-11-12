"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
   model for python internal SQLite db
"""
from webapp.db import DB


class Recipe(DB.Model):
    """ Recipe table """
    __tablename__ = "recipe"
    id = DB.Column(DB.Integer, primary_key=True)
    author_id = DB.Column(DB.Integer)
    dish_type = DB.Column(DB.String(100))
    cusine_type = DB.Column(DB.String(100))
    name = DB.Column(DB.String(300))
    cooking = DB.Column(DB.String(2000))
    minutes = DB.Column(DB.Integer)
    old_id = DB.Column(DB.Integer)

    def __repr__(self):
        """repr method"""
        return f"<Recipe {self.id} {self.name}>"


class Ingredient(DB.Model):
    __tablename__ = "ingredient"
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(160), index=True, unique=False)

    def __repr__(self):
        """repr method"""
        return f"<Ingredient {self.id} {self.name}>"


class Measure(DB.Model):
    """ table with Measures """
    __tablename__ = "measure"
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(160), index=True, unique=False)

    def __repr__(self):
        """repr method"""
        return f"<Measure {self.id} {self.name}>"


class IngredientGroup(DB.Model):
    """IngredientGroup table"""
    __tablename__ = "ingredient_group"
    id = DB.Column(DB.Integer, primary_key=True)
    ingredient_id = DB.Column(DB.Integer, DB.ForeignKey("ingredient.id"))
    ingredients = DB.relationship("Ingredient",
                                  backref=DB.backref("ingredient_group"))
    measure_id = DB.Column(DB.Integer, DB.ForeignKey("measure.id"))
    measures = DB.relationship("Measure",
                               backref=DB.backref("ingredient_group"))

    def __repr__(self):
        """repr method"""
        return f"<IngredientGroup recipe{self.recipe_id} {self.ingredient_id}>"


class Author(DB.Model):
    """Ingredient model"""
    __tablename__ = "author"
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(128), index=True, unique=False)

    def __repr__(self):
        """repr method"""
        return f"<Author {self.id} {self.name}>"


class Interactions(DB.Model):
    """Interactions model for collaborative filtering"""
    __tablename__ = "interactions"
    author_id = DB.Column(DB.Integer, primary_key=True)
    recipe_id = DB.Column(DB.Integer, primary_key=True)
    created = DB.Column(DB.Date)
    rating = DB.Column(DB.Float)

    def __repr__(self):
        """repr method"""
        return f"<Interaction {self.author_id} {self.recipe_id}>"


class Recipes(DB.Model):
    """ Recipes table """
    __tablename__ = "recipes"
    id = DB.Column(DB.Integer, primary_key=True)
    creator_id = DB.Column(DB.Integer)
    dish_type = DB.Column(DB.String(64))
    cusine_type = DB.Column(DB.String(64))
    name = DB.Column(DB.String(300))
    cooking_directions = DB.Column(DB.String(2000))
    pic_url = DB.Column(DB.String(300))
    pic = DB.Column(DB.String(100))
    ingredient_group_id = DB.Column(DB.Integer,
                                    DB.ForeignKey("ingredient_group.id"))
    ingredient_group = DB.relationship('IngredientGroup',
                                       backref=DB.backref('recipes',
                                                          uselist=False))

    def __repr__(self):
        """repr method"""
        return f"<Recipes object {self.id} {self.name}>"


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
        return f"<temp note {self.id} {self.name}>"
