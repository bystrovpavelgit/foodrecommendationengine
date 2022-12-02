""" Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    script to load ratings """
import csv
from datetime import date
import numpy as np
from webapp import create_app
from webapp.business_logic import insert_authors, insert_interactions


def process_authors_from_file(name="data/authors.csv"):
    """ process authors from file """
    res = []
    try:
        with open(name, "r") as f:
            fields = ['user_id', 'name']
            rows = csv.DictReader(f, fields, delimiter=',')
            res = [{"id": int(row["user_id"]), "name": row["name"]} for row in
                   rows if row["user_id"] != "user_id"]
            insert_authors(res)
    except FileNotFoundError:
        print(f"File not found: {name}")
    return res


def process_recipe_ratings_from_file(name="data/recipe_ratings.csv"):
    """ process recipe ratings from file """
    try:
        with open(name, "r") as f:
            fields = ['user_id', 'recipe_id', 'rating']
            rows = csv.DictReader(f, fields, delimiter=',')
            res = [{"author_id": int(row["user_id"]),
                    "recipe_id": int(row["recipe_id"]),
                    "rating": float(row["rating"])} for row in
                   rows if row["user_id"] != "user_id"]
            n = len(res)
            rands = np.random.randn(n)
            maxx, minn = np.max(np.abs(rands)), np.min(rands)
            rands = ((rands - minn) / maxx) * 100
            for k in range(n):
                dat = date.today()
                res[k]["created"] = date.fromisocalendar(dat.year, 1 + int(rands[k]) // 7, 1 + int(rands[k]) % 7)
            insert_interactions(res)
    except FileNotFoundError:
        print(f"File not found: {name}")
    return res


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # load all authors
        result = process_authors_from_file(name="data/authors.csv")
        print(f"{len(result)} authors loaded")
        # load all interactions
        result = process_recipe_ratings_from_file(name="data/recipe_ratings.csv")
        print(f"{len(result)} ratings loaded")
