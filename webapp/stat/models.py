"""
   author Pavel Bystrov
   models for internal SQLite db
"""
from webapp.db import DB


class Ingredient(DB.Model):
    """ table with Ingredients """
    __tablename__ = "ingredient"
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(160), index=True, unique=False)

    def __repr__(self):
        """repr method"""
        return f"<Ingredient {self.id} {self.name}>"


class IngredientGroup(DB.Model):
    """IngredientGroup table"""
    __tablename__ = "ingredient_group"
    id = DB.Column(DB.Integer, primary_key=True)
    recipe_id = DB.Column(DB.Integer, DB.ForeignKey('recipe.id'), nullable=False)
    recipes = DB.relationship('Recipe', backref=DB.backref('IngredientGroup', uselist=False))
    ingredient_id = DB.Column(DB.Integer, DB.ForeignKey("ingredient.id"), nullable=False)
    ingredients = DB.relationship('Ingredient', backref=DB.backref('IngredientGroup', uselist=False))
    mera = DB.Column(DB.String(100))

    def __repr__(self):
        """repr method"""
        return f"<IngredientGroup recipe_id: {self.recipe_id} ingredient_id: {self.ingredient_id}>"


class Recipe(DB.Model):
    """ Recipes table """
    __tablename__ = "recipe"
    id = DB.Column(DB.Integer, primary_key=True)
    creator_id = DB.Column(DB.Integer)
    dish_type = DB.Column(DB.String(120))
    cuisine_type = DB.Column(DB.String(120))
    name = DB.Column(DB.String(200))
    cooking = DB.Column(DB.String(2000))

    def __repr__(self):
        """repr method"""
        return f"<Recipe {self.id} {self.name}>"


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
    rating = DB.Column(DB.Float)

    def __repr__(self):
        """repr method"""
        return f"<Interactions {self.author_id} {self.recipe_id} {self.rating}>"


