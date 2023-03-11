"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    business logic for dish recommendations
"""
import csv
from datetime import date
import logging
from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError, PendingRollbackError
from webapp.db import DB
from webapp.stat.models import Note, Author, Interactions
from webapp.user.models import User


def save_users_ratings(file_name="data/users_ratings.csv"):
    """ save ratings to users_ratings.csv """
    try:
        with open(file_name, "w", encoding="utf-8") as newfile:
            fields = ["userId", "rating", "recipeId"]
            writer = csv.DictWriter(newfile, fields, delimiter=',')
            writer.writeheader()
            for row in Interactions.query.all():
                row_dict = {
                    fields[0]: row.author_id,
                    fields[1]: int(row.rating),
                    fields[2]: row.recipe_id
                }
                writer.writerow(row_dict)
    except FileNotFoundError:
        logging.error(f"File not found: {file_name}")


def log_sql_error(an_exception: Exception, comments: str) -> None:
    """ log sql error """
    error = str(an_exception.__dict__['orig'])
    msg = f"Exception {error} {comments}"
    logging.error(msg)


def log_error_and_rollback(new_exception: Exception, comment: str) -> None:
    """ log sql error and call rollback() """
    log_sql_error(new_exception, comment)
    DB.session.rollback()


def bulk_insert(clazz, data):
    """ insert multiple authors """
    if data:
        try:
            DB.session.bulk_insert_mappings(Author, data)
            DB.session.commit()
        except (SQLAlchemyError, IntegrityError, PendingRollbackError) as exc:
            log_error_and_rollback(exc, f"in bulk_insert({clazz}, {data})")


def get_user_by_name(name):
    """  find user by name """
    try:
        user = User.query.filter_by(username=name).first()
        return user
    except (SQLAlchemyError, IntegrityError) as exc:
        log_sql_error(exc, f"in get_user_by_name({name})")
        return None


def find_recipe_names(cuisine):
    """ find recipe names """
    result = [""] * 9
    ids = [-1] * 9
    try:
        if Note.query.filter(Note.cusine == cuisine).count() > 0:
            notes = Note.query.filter(
                Note.cusine == cuisine).order_by(Note.id).limit(9)
            result = [data.name for data in notes]
            ids = [data.id for data in notes]
    except (SQLAlchemyError, IntegrityError) as exc:
        log_sql_error(exc, f"in find_recipe_names({cuisine})")
    return result, ids


def get_recipe_names_by_cuisine(ids, cuisine):
    """ find recipe names by cuisine """
    result = []
    res_ids = []
    try:
        for data in Note.query.filter(
                Note.cusine == cuisine).filter(Note.id.in_(ids)).all():
            result.append(data.name)
            res_ids.append(data.id)
    except SQLAlchemyError as exc:
        log_sql_error(exc,
                      f"in get_recipe_names_by_cuisine({cuisine})")
    return result, res_ids


def get_recipe_names_by_type(ids, type_):
    """ find recipe names by type """
    result = []
    res_ids = []
    try:
        for data in Note.query.filter(
                Note.typed == type_).filter(Note.id.in_(ids)).all():
            result.append(data.name)
            res_ids.append(data.id)
    except SQLAlchemyError as exc:
        log_sql_error(exc, f"in get_recipe_names_by_type({type_})")
    return result, res_ids


def find_recipe(id_):
    """ find recipe by id """
    note = None
    try:
        if Note.query.filter(Note.id == id_).count() > 0:
            note = Note.query.filter(Note.id == id_).first()
    except (SQLAlchemyError, IntegrityError) as exc:
        log_sql_error(exc, f"in find_recipe({id_})")
    return note


def insert_or_update_rating(rating, name, recipe_id):
    """ insert or update rating for author """
    if name:
        author_id = None
        try:
            author = Author.query.filter(Author.name == name).first()
            author_id = author.id if author else -1
            cur_date = date.today()
            if Interactions.query.filter(
                    Interactions.author_id == author_id and
                    Interactions.recipe_id == recipe_id).count() == 0:
                DB.session.add(Interactions(rating=rating,
                                            author_id=author_id,
                                            recipe_id=recipe_id,
                                            created=cur_date))
            else:
                interact = Interactions.query.filter(
                    Interactions.author_id == author_id and
                    Interactions.recipe_id == recipe_id).first()
                interact.rating = rating
                interact.created = cur_date
            logging.debug(f"insert/update Interactions: rating:{rating} " +
                          f"rid:{recipe_id} aid:{author_id}")
            DB.session.commit()
        except (SQLAlchemyError, IntegrityError, PendingRollbackError) as exc:
            log_error_and_rollback(exc,
                                   "in insert_or_update_rating(rating:" +
                                   f"{rating} aid:{author_id} rid:{recipe_id}")


def find_recipe_id_by_type_and_cuisine(dish_type, cusine):
    """ find recipe id by type and cuisine """
    id_ = None
    try:
        if Note.query.filter(
                Note.cusine == cusine).filter(Note.typed == dish_type).count() > 0:
            recipe = Note.query.filter(
                Note.cusine == cusine).filter(Note.typed == dish_type).first()
            id_ = recipe.id
    except (SQLAlchemyError, IntegrityError) as exc:
        log_sql_error(exc, "in find_recipe_id_by_type_and_cuisine()")
    return id_


def insert_recipe_data(data):
    """ insert data for recipe """
    if data:
        try:
            DB.session.bulk_insert_mappings(Note, data)
            DB.session.commit()
        except (SQLAlchemyError, IntegrityError, PendingRollbackError) as exc:
            log_error_and_rollback(exc, f"in insert_recipe_data({data})")


def delete_recipe_data(id_):
    """ delete recipe data """
    try:
        if Note.query.filter(Note.id == id_).count() == 0:
            return False
        note = Note.query.filter(Note.id == id_).first()
        DB.session.delete(note)
        DB.session.commit()
        return True
    except (SQLAlchemyError, IntegrityError, PendingRollbackError) as exc:
        log_error_and_rollback(exc, f"in delete_recipe_data({id_})")
    return False
