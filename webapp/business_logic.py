"""business logic"""
from bs4 import BeautifulSoup
from webapp.db import DB
from webapp.stat.models import Note
import requests


def find_data_by_cuisine(search, cuisine):
    """ find recipe by cuisine """
    tmp = search
    if Note.query.filter(Note.cusine == cuisine).count() > 0:
        return Note.query.filter(Note.cusine == cuisine).first()


def insert_recipe_data(data):
    """ insert data for recipe """
    if data:
        DB.session.bulk_insert_mappings(Note, data)
        DB.session.commit()
    return ""


def delete_recipe_data(id_):
    """ insert data for recipe """
    if Note.query.filter(Note.id == id_).count() == 0:
        return False
    note = Note.query.filter(Note.id == id_).first()
    DB.session.delete(note)
    DB.session.commit()
    return True


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("error")
        return False


def get_python_news(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        html = result.text
    except(requests.RequestException, ValueError):
        print("error")
        return False

    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.find("ul", class_="list-recent-posts").findAll("li")
        result_news = []
        for news in all_news:
            title = news.find("a").text
            url = news.find("a")["href"]
            published = news.find("time").text
            print(title, url, published)
            result_news.append((title, url, published))
        return result_news
    return False
