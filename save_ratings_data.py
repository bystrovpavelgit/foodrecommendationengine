""" Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    script to save ratings for CF model"""
from webapp import create_app
from webapp.business_logic import save_users_ratings


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # save all ratings
        save_users_ratings(file_name="data/users_ratings.csv")
        print(f"ratings saved as users_ratings.csv")
