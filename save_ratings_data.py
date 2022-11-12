""" script to save ratings for CF model"""
import csv
from webapp import create_app
from webapp.stat.models import Interactions


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # load all authors
        with open("data/users_ratings.csv", "w") as f:
            fields = ["userId", "rating", "recipeId"]
            writer = csv.DictWriter(f, fields, delimiter=',')
            writer.writeheader()
            for row in Interactions.query.all():
                row_dict = {fields[0]: row.author_id,
                            fields[1]: int(row.rating),
                            fields[2]: row.recipe_id,
                            }
                writer.writerow(row_dict)
        print(f"ratings saved as users_ratings.csv")
