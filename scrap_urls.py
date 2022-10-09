""" scrapper for list of urls """
import json
import time
from webapp.utils.web_util import get_html
from webapp.utils.scrapper_util import load_eda_ru_urls

if __name__ == "__main__":
    cusine_map = {"/russkaya-kuhnya": 'русская',
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
    for element in reversed(list(cusine_map.items())):
        for type_ in reversed(list(types.items())):
            url = "https://eda.ru/recepty" + element[0] + type_[0]
            time.sleep(9)
            html = get_html(url)
            print(element[0], type_[0])
            if html:
                urls = load_eda_ru_urls(html)
                for url_ in urls:
                    dish_list.append({"url": url_, "cusine": element[1], "type": type_[1]})
    with open("dishes.json", "w", encoding="utf-8") as f:
        json.dump(dish_list, f)
    print("Done")
