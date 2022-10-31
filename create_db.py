""" author Pavel Bystrov
    create database """
from webapp.db import DB
from webapp import create_app

if __name__ == "__main__":
    app=create_app()
    DB.create_all(app=app)
