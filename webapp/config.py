"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    web-app configuration
"""
import logging
import os
from datetime import timedelta

logging.basicConfig(filename='webapp.log', level=logging.INFO)
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir,
                                                      "..",
                                                      "webapp.db")
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "QWEWQYUhj342678gvmjhxckbdvkjbsabc"
REMEMBER_COOKIE_DURATION = timedelta(days=7)
COLORS = ["table-primary", "table-secondary", "table-info", "table-light",
          "table-success"]
RECOMMEND_ACTIONS = [f"Рецепт {n}" for n in range(1, 10)]
RATE_ACTIONS = [str(n) for n in range(1, 8)]
RECOMMEND_ACT = "action_"
RATE_ACT = "action"
VALID_CUISINE = ["европейская", "русская", "азиатская", "африканская",
                 "мексиканская"]
TYPE_MAP = {"вторые блюда": 1,
            "десерты": 2,
            "завтраки": 3,
            "закуски": 4,
            "салаты": 5,
            "соусы": 6,
            "супы и первые блюда": 7,
            }
FILL_RECIPE = "Заполните Рецепт"
INGREDIENTS_NUM = "Количество Ингредиентов"
RECIPE = "Рецепт"
CALC_MODEL = "Обновление модели"


