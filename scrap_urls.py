""" Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    scrapper for list of urls """
import json
import time
from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from webapp import create_app
from webapp.db import DB
from webapp.stat.models import Note
from webapp.utils.web_util import get_html
from webapp.utils.scrapper_util import load_eda_ru_urls, extract_recipe


def get_dishes(url_link, element, dish_type, num):
    """ get_links function - attrs: url_link, element, type_ num """
    dishes = []
    html = get_html(url_link + f"?page={num}")
    print(element, dish_type)
    if html:
        urls = load_eda_ru_urls(html)
        for url_ in urls:
            dishes.append({"url": url_, "cusine": element, "type": dish_type})
    return dishes


def get_loaded_urls():
    """ loaded urls """
    try:
        res = Note.query.limit(9000)
        result = [note.url for note in res]
        return result
    except (SQLAlchemyError, IntegrityError) as ex:
        error = str(ex.__dict__['orig'])
        print(f"exception in Note table {error}")
        raise ex


def get_recipe_urls(cuisine_dict, types_dict):
    """
       load recipe urls from eda.ru using cusine_map
       and types dictionary
    """
    dishes = []
    for element in cuisine_dict.items():
        for type_ in types_dict.items():
            link = "https://eda.ru/recepty" + element[0] + type_[0]
            for j in range(6):
                time.sleep(5)
                dishes = dishes + get_dishes(link, element[1], type_[1], j)
    return dishes


def save_recipe(recipe, dish_dict, url_link):
    """ save recipe details """
    if recipe:
        name, photo, ingredient_list, items, dirs = extract_recipe(recipe)
        try:
            note = Note(name=name,
                        pic_url=photo,
                        pic="",
                        ingredients=f"{ingredient_list}",
                        mera=f"{items}",
                        directions=f"{dirs}",
                        cusine=dish_dict["cusine"],
                        typed=dish_dict["type"],
                        url=url_link)
            DB.session.add(note)
            DB.session.commit()
        except (SQLAlchemyError, IntegrityError) as ex:
            error = str(ex.__dict__['orig'])
            print(f"exception in insert {error}")
            DB.session.rollback()


if __name__ == "__main__":
    cuisine_map = {"/russkaya-kuhnya": 'русская',
                   "/afikanskaya-kuhnya": 'африканская',
                   "/meksikanskaya-kuhnya": 'мексиканская',
                   "/serbskaya-kuhnya": "сербская",
                   "/tureckaya-kuhnya": 'азиатская',
                   "/evropeyskaya-kuhnya": 'европейская',
                   "/vengerskaya-kuhnya": 'венгерская',
                   "/indiyskaya-kuhnya": 'азиатская',
                   "/francuzskaya-kuhnya": 'европейская',
                   "/kitayskaya-kuhnya": 'азиатская',
                   "/yaponskaya-kuhnya": 'азиатская',
                   "/armyanskaya-kuhnya": 'европейская',
                   "/ispanskaya-kuhnya": 'европейская',
                   "/azerbaydzhanskaya-kuhnya": 'европейская',
                   "/koreyskaya-kuhnya": 'азиатская',
                   "/tayskaya-kuhnya": 'азиатская',
                   "/uzbekskaya-kuhnya": 'азиатская',
                   "/arabskaya-kuhnya": 'азиатская',
                   "/marokkanskaya-kuhnya": 'африканская',
                   "/vetnamskaya-kuhnya": 'азиатская',
                   "/panaziatskaya-kuhnya": 'азиатская',
                   "/tatarskaya-kuhnya": 'русская',
                   "/sredizemnomorskaya-kuhnya": 'европейская',
                   "/belorusskaya-kuhnya": 'русская',
                   "/avstriyskaya-kuhnya": 'европейская',
                   "/irlandskaya-kuhnya": 'европейская',
                   "/argentinskaya-kuhnya": 'мексиканская',
                   "/brazilskaya-kuhnya": 'мексиканская',
                   "/osetinskaya-kuhnya": 'русская'
                   }
    types = {"/vypechka-deserty": 'десерты',
             "/osnovnye-blyuda": "вторые блюда",
             "/zavtraki": 'завтраки',
             "/salaty": "салаты",
             "/supy": 'супы и первые блюда',
             "/zakuski": 'закуски',
             "/sousy-marinady": "соусы",
             "/pasta-picca": "вторые блюда",
             "/rizotto": "вторые блюда",
             "/bulony": 'супы и первые блюда',
             "/sendvichi": 'закуски',
             }
    # load dish list
    dish_list = get_recipe_urls(cuisine_map, types)
    # save dishes.json
    with open("dishes.json", "w", encoding="utf-8") as f:
        json.dump(dish_list, f)
    print("Done with dish_list")
    app = create_app()
    # load dish objects using url
    with app.app_context():
        loaded = get_loaded_urls()
        for dish in dish_list:
            url = dish["url"]
            if url in loaded:
                continue
            print(url)
            time.sleep(7)
            detail = get_html(url)
            save_recipe(detail, dish, url)
    print("Done loading recipes")
