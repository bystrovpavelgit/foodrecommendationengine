"""
    download all recipes
    please run python3 scrap_urls.py before running this script
"""
import json
import time
from webapp import create_app
from webapp.db import DB
from webapp.stat.models import Note
from webapp.utils.web_util import get_html
from webapp.utils.scrapper_util import extract_recipe, get_image


if __name__ == "__main__":
    with open("dishes.json", "r", encoding="utf-8") as f:
        dish_list = json.load(f)
    app = create_app()
    BASE_DIR = "./webapp/templates/img/"
    with app.app_context():
        for dish in dish_list:
            time.sleep(12)
            url = dish["url"]
            print(url)
            detail = get_html(url)
            if detail:
                name, photo, ingredient_list, items, dirs = extract_recipe(detail)
                image = get_image(photo, BASE_DIR) if photo else ""
                note = Note(name=name,
                            pic_url=photo,
                            pic=image,
                            ingredients=f"{ingredient_list}",
                            mera=f"{items}",
                            directions=f"{dirs}",
                            cusine=dish["cusine"],
                            typed=dish["cusine"],
                            url=url)
                DB.session.add(note)
                DB.session.commit()
        total = Note.query.count()
        print("Done loading {total} recipes with images")
