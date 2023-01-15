"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    business logic for dish recommendations
"""
import csv
from datetime import date
import logging
from sqlalchemy.exc import SQLAlchemyError, PendingRollbackError
from sqlite3 import IntegrityError
from webapp.db import DB
from webapp.stat.models import Note, Author, Interactions
from webapp.user.models import User


def save_users_ratings(file_name="data/users_ratings.csv"):
    """ save ratings to users_ratings.csv """
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            fields = ["userId", "rating", "recipeId"]
            writer = csv.DictWriter(f, fields, delimiter=',')
            writer.writeheader()
            for row in Interactions.query.all():
                row_dict = {fields[0]: row.author_id,
                            fields[1]: int(row.rating),
                            fields[2]: row.recipe_id,
                            }
                writer.writerow(row_dict)
    except FileNotFoundError:
        logging.error("File not found: {file_name}")


def insert_authors(data):
    """ insert multiple authors """
    if data:
        try:
            DB.session.bulk_insert_mappings(Author, data)
            DB.session.commit()
        except (SQLAlchemyError, IntegrityError, PendingRollbackError) as e:
            error = str(e.__dict__['orig'])
            err = f"Exception in insert_authors: {error} "
            logging.error(err)
            DB.session.rollback()


def insert_interactions(data):
    """ insert multiple interactions """
    if data:
        try:
            DB.session.bulk_insert_mappings(Interactions, data)
            DB.session.commit()
        except (SQLAlchemyError, IntegrityError, PendingRollbackError) as e:
            error = str(e.__dict__['orig'])
            err = f"Exception in insert_authors: {error} "
            logging.error(err)
            DB.session.rollback()


def get_user_by_name(name):
    """  get user by name """
    try:
        user = User.query.filter_by(username=name).first()
        return user
    except (SQLAlchemyError, IntegrityError) as e:
        error = str(e.__dict__['orig'])
        err = f"Exception in get_user_by_name: {error} / {name} "
        logging.error(err)


def find_recipe_names(cuisine):
    """ find recipe names """
    result = [""] * 9
    ids = [-1] * 9
    if Note.query.filter(Note.cusine == cuisine).count() > 0:
        try:
            notes = Note.query.filter(
                Note.cusine == cuisine).order_by(Note.id).limit(9)
            result = [data.name for data in notes]
            ids = [data.id for data in notes]
        except (SQLAlchemyError, IntegrityError) as e:
            error = str(e.__dict__['orig'])
            err = f"Exception in find_recipe_names: {error} / {cuisine} "
            logging.error(err)
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
    try:
        if Note.query.filter(Note.id == id_).count() > 0:
            note = Note.query.filter(Note.id == id_).first()
            return note
    except (SQLAlchemyError, IntegrityError) as e:
        error = str(e.__dict__['orig'])
        err = f"recipe {id_} not found: {error}"
        logging.error(err)


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
                logging.debug(f"insert Interactions: aid:{author_id} " +
                              f"rid:{recipe_id} rating:{rating}")
            else:
                interact = Interactions.query.filter(
                    Interactions.author_id == author_id and
                    Interactions.recipe_id == recipe_id).first()
                interact.rating = rating
                interact.created = cur_date
                logging.debug(f"update Interactions: aid:{author_id} " +
                              f"rid:{recipe_id} rating:{rating}")
            DB.session.commit()
        except (SQLAlchemyError, IntegrityError, PendingRollbackError) as e:
            error = str(e.__dict__['orig'])
            err = f"Exception in insert_or_update_rating: {error} " + \
                  f"aid:{author_id} rid:{recipe_id} rating:{rating}"
            logging.error(err)
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
        try:
            DB.session.bulk_insert_mappings(Note, data)
            DB.session.commit()
        except (SQLAlchemyError, IntegrityError, PendingRollbackError) as e:
            error = str(e.__dict__['orig'])
            err = f"Exception in insert_recipe_data: {error} / {data} "
            logging.error(err)
            DB.session.rollback()


def delete_recipe_data(id_):
    """ insert data for recipe """
    if Note.query.filter(Note.id == id_).count() == 0:
        return False
    try:
        note = Note.query.filter(Note.id == id_).first()
        DB.session.delete(note)
        DB.session.commit()
        return True
    except (SQLAlchemyError, IntegrityError, PendingRollbackError) as e:
        error = str(e.__dict__['orig'])
        err = f"Exception in delete_recipe_data: {error} / {id_} "
        logging.error(err)
        DB.session.rollback()
    return False
