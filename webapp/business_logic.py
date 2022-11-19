"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    business logic functionality
"""
from datetime import date
import logging
from sqlalchemy.exc import SQLAlchemyError, PendingRollbackError
from sqlite3 import IntegrityError
from webapp.db import DB
from webapp.stat.models import Note, Author, Interactions
from webapp.user.models import User


def get_user_by_name(name):
    """  get user by name """
    user = User.query.filter_by(username=name).first()
    return user


def find_recipe_names(cuisine):
    """ find recipe names """
    result = [""] * 9
    ids = [-1] * 9
    if Note.query.filter(Note.cusine == cuisine).count() > 0:
        notes = Note.query.filter(
            Note.cusine == cuisine).order_by(Note.id).limit(9)
        result = [data.name for data in notes]
        ids = [data.id for data in notes]
    return result, ids


def get_recipe_names_by_cuisine(ids, cuisine):
    """ find recipe names by cuisine """
    result = []
    res_ids = []
    for data in Note.query.filter(
            Note.cusine == cuisine).filter(Note.id.in_(ids)).all():
        result.append(data.name)
        res_ids.append(data.id)
    return result, res_ids


def get_recipe_names_by_type(ids, type_):
    """ find recipe names by type """
    result = []
    res_ids = []
    for data in Note.query.filter(
            Note.typed == type_).filter(Note.id.in_(ids)).all():
        result.append(data.name)
        res_ids.append(data.id)
    return result, res_ids


def find_recipe(id_):
    """ find recipe by id """
    if Note.query.filter(Note.id == id_).count() > 0:
        note = Note.query.filter(Note.id == id_).first()
        return note


def insert_or_update_rating(rating, name, recipe_id):
    """ insert or update rating for author """
    if name:
        author = Author.query.filter(Author.name == name).first()
        author_id = author.id if author else -1
        cur_date = date.today()
        try:
            if Interactions.query.filter(
                    Interactions.author_id == author_id and
                    Interactions.recipe_id == recipe_id).count() == 0:
                DB.session.add(Interactions(rating=rating,
                                            author_id=author_id,
                                            recipe_id=recipe_id,
                                            created=cur_date))
                logging.debug(f"insert Interactions: aid:{author_id} rid:{recipe_id} rating:{rating}")
            else:
                interact = Interactions.query.filter(
                    Interactions.author_id == author_id and
                    Interactions.recipe_id == recipe_id).first()
                interact.rating = rating
                interact.created = cur_date
                logging.debug(f"update Interactions: aid:{author_id} rid:{recipe_id} rating:{rating}")
            DB.session.commit()
        except (SQLAlchemyError, IntegrityError, PendingRollbackError) as e:
            error = str(e.__dict__['orig'])
            err = f"Exception in insert_or_update_rating: {error} " + \
                  f"aid:{author_id} rid:{recipe_id} rating:{rating}"
            logging.debug(err)
            DB.session.rollback()


def find_recipe_id_by_type_and_cuisine(dish_type, cusine):
    """ find recipe by cuisine """
    if Note.query.filter(
            Note.cusine == cusine).filter(Note.typed == dish_type).count() > 0:
        recipe = Note.query.filter(
            Note.cusine == cusine).filter(Note.typed == dish_type).first()
        return recipe.id


def insert_recipe_data(data):
    """ insert data for recipe """
    if data:
        DB.session.bulk_insert_mappings(Note, data)
        DB.session.commit()


def delete_recipe_data(id_):
    """ insert data for recipe """
    if Note.query.filter(Note.id == id_).count() == 0:
        return False
    note = Note.query.filter(Note.id == id_).first()
    DB.session.delete(note)
    DB.session.commit()
    return True
