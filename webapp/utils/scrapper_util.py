"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    scrapper utility
"""
import json
import os
import time
import requests
from bs4 import BeautifulSoup
from requests import ReadTimeout, ConnectTimeout, Timeout
from requests.exceptions import HTTPError


def load_eda_ru_urls(html):
    """ extract urls from html page"""
    soup = BeautifulSoup(html, 'html.parser')
    news_list = soup.find_all("script")
    txt = str(news_list[-1]).replace("</script>", "") \
        .replace('<script id="__NEXT_DATA__" type="application/json">', "")
    data = json.loads("[" + txt + "]")
    result = [str(e["url"].replace("/recepty/recepty", "/recepty")) for e in
              data[0]["props"]["pageProps"]["metaData"]['microdata']['itemListElement']]
    return result


def get_another_photo(soup):
    """ search other url source inside div tag with item-prop='recipeInstructions'
    and in meta tag with itemProp=image """
    item = soup.find("div", itemprop="recipeInstructions")
    if item:
        results = item.find_all("img", class_="emotion-1vbvoti")
        if results:
            res = results.pop()
            if 'src' in res.attrs:
                src = res.attrs["src"]
                return src


def get_photo_url(soup):
    """ get photo url source """
    item = soup.find("div", class_="emotion-mrkurn")
    if item:
        results = item.find_all("img")
        if results:
            res = results.pop(0)
            if 'src' in res.attrs:
                src = res.attrs["src"]
                return src
    url = get_another_photo(soup)
    return url


def get_ingredients(soup):
    """ get_ingredients function """
    ingrs = soup.find_all("div", class_="emotion-ydhjlb")
    ingredients_list = [i.find_next("span", itemprop="recipeIngredient").text for i in ingrs]
    result = [i.find_next("span", class_="emotion-15im4d2").text for i in ingrs]
    n = len(ingredients_list)
    if n > 3 and ingredients_list[0] == ingredients_list[1] and \
            ingredients_list[0] == ingredients_list[2]:
        return ingredients_list[2:], result[2:]
    return ingredients_list, result


def get_directions(soup):
    """ get_directions function """
    directions = soup.find_all("span", class_="emotion-6kiu05")
    if len(directions) > 0:
        res = [e.find_next("span",
                           itemprop="text").text.replace("\xa0", " ") for e in directions]
        return res


def get_dish_name(soup):
    """ function to extract dish name """
    name = soup.find("h1", class_="emotion-gl52ge")
    txt = name.text
    return txt


def get_image(url, directory="./"):
    """ load remote image and save it to directory """
    tmp_index = url.rfind("/")
    index = url[:tmp_index].rfind("/") + 1
    img_name = url[index:].replace("/", "-")
    try:
        time.sleep(9)
        img_request = requests.get(url, timeout=8.0)
        img_request.raise_for_status()
        with open(os.path.join(directory, img_name), "wb") as img:
            img.write(img_request.content)
            img.close()
            return img_name
    except (ConnectTimeout, ReadTimeout, Timeout, ConnectionError, HTTPError):
        print("connection error")
    except(requests.RequestException, ValueError):
        print('ошибка')
    return ""


def extract_recipe(html):
    """ get_python_news function"""
    soup = BeautifulSoup(html, 'html.parser')
    dish = get_dish_name(soup)
    photo = get_photo_url(soup)
    ingredients, nums = get_ingredients(soup)
    dirs = get_directions(soup)
    return dish, photo, ingredients, nums, dirs
