""" script to load ratings"""
import csv
from datetime import date
import numpy as np
from webapp import create_app
from webapp.db import DB
from webapp.stat.models import Author, Interactions


def insert_authors(data):
    """ insert multiple authors """
    if data:
        DB.session.bulk_insert_mappings(Author, data)
        DB.session.commit()


def insert_interactions(data):
    """ insert multiple interactions """
    if data:
        DB.session.bulk_insert_mappings(Interactions, data)
        DB.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # load all authors
        with open("data/authors.csv", "r") as f:
            fields = ['user_id', 'name']
            rows = csv.DictReader(f, fields, delimiter=',')
            result = [{"id": int(row["user_id"]), "name": row["name"]} for row in rows if row["user_id"] != "user_id"]
            insert_authors(result)
        print(f"{len(result)} authors loaded")
        # load all interactions
        with open("data/recipe_ratings.csv", "r") as f:
            fields = ['user_id', 'recipe_id', 'rating']
            rows = csv.DictReader(f, fields, delimiter=',')
            result = [{"author_id": int(row["user_id"]),
                       "recipe_id": int(row["recipe_id"]),
                       "rating": float(row["rating"])} for row in rows if row["user_id"] != "user_id"]
            n = len(result)
            rands = np.random.randn(n)
            maxx, minn = np.max(np.abs(rands)), np.min(rands)
            rands = ((rands - minn) / maxx) * 100
            for k in range(n):
                dat = date.today()
                result[k]["created"] = date.fromisocalendar(dat.year, 1 + int(rands[k]) // 7, 1 + int(rands[k]) % 7)
            insert_interactions(result)
        print(f"{len(result)} ratings loaded")
