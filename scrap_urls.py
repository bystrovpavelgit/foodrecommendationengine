""" Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    scrapper for list of urls """
import json
import time
from webapp.utils.web_util import get_html
from webapp.utils.scrapper_util import load_eda_ru_urls


def get_links(url, element, type_, num):
    """ get_links function - attrs: url, element, type_ num """
    dish_list = []
    html = get_html(url + f"?page={num}")
    print(element, type_)
    if html:
        urls = load_eda_ru_urls(html)
        for url_ in urls:
            dish_list.append({"url": url_, "cusine": element, "type": type_})
    return dish_list


if __name__ == "__main__":
    # "/russkaya-kuhnya": 'русская',
    # "/afikanskaya-kuhnya": 'африканская',
    # "/meksikanskaya-kuhnya": 'мексиканская',
    # "/serbskaya-kuhnya": "сербская",
    # "/tureckaya-kuhnya": 'азиатская',
    # "/evropeyskaya-kuhnya": 'европейская',
    # "/vengerskaya-kuhnya": 'венгерская',
    # "/indiyskaya-kuhnya": 'азиатская',
    # "/francuzskaya-kuhnya": 'европейская',
    # "/kitayskaya-kuhnya": 'азиатская',
    # "/yaponskaya-kuhnya": 'азиатская',
    # "/armyanskaya-kuhnya": 'европейская',
    # "/ispanskaya-kuhnya": 'европейская',
    # "/azerbaydzhanskaya-kuhnya": 'европейская',
    # "/koreyskaya-kuhnya": 'азиатская',
    # "/tayskaya-kuhnya": 'азиатская',
    # "/uzbekskaya-kuhnya": 'азиатская',
    # "/arabskaya-kuhnya": 'азиатская',
    # "/marokkanskaya-kuhnya": 'африканская',
    # "/vetnamskaya-kuhnya": 'азиатская',
    cusine_map = {"/panaziatskaya-kuhnya": 'азиатская',
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
    dish_list = []
    for element in cusine_map.items():
        for type_ in types.items():
            url = "https://eda.ru/recepty" + element[0] + type_[0]
            for j in range(6):
                time.sleep(6)
                lst = get_links(url, element[1], type_[1], j)
                dish_list = dish_list + lst

    with open("more_dishes3.json", "w", encoding="utf-8") as f:
        json.dump(dish_list, f)
    print("Done")
