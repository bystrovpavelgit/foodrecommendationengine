"""
    to download all recipes
    please run python3 scrap_urls.py before running this script
"""
from webapp import create_app
from webapp.db import DB
from webapp.stat.models import Note
from webapp.utils.nlp_util import str_to_list


def convert_str_to_array(text):
    """ convert str to array """
    result = [s.replace(",", ".")
              for s in text.split("'")
              if (not s.startswith(",")) and s != "[" and s != "]"]
    if len(result) > 2 and result[0] == result[2] and result[0] == result[1]:
        result = result[2:]
    return result


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        for data in Note.query.all():
            items = convert_str_to_array(data.ingredients)
            mera = convert_str_to_array(data.mera)
            recipe_text = " ".join(str_to_list(data.directions))
            data.ingredients = f"{items}"
            data.mera = f"{mera}"
            data.directions = recipe_text
        DB.session.commit()
