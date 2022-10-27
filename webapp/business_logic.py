""" business logic functionality """
from datetime import date
from bs4 import BeautifulSoup
from webapp.db import DB
from webapp.stat.models import Note, Author, Interactions
from webapp.utils.web_util import get_html


def find_recipe_names(cuisine):
    """ find recipe names """
    result = [""] * 9
    ids = [-1] * 9
    if Note.query.filter(Note.cusine == cuisine).count() > 0:
        notes = Note.query.filter(Note.cusine == cuisine).order_by(Note.id).limit(9)
        result = [data.name for data in notes]
        ids = [data.id for data in notes]
    return result, ids


def find_recipe(id_):
    """ find recipe by id """
    if Note.query.filter(Note.id == id_).count() > 0:
        note = Note.query.filter(Note.id == id_).first()
        return note


def insert_or_update_rating(rating, name, recipe_id):
    """ insert or update rating for author """
    if name:
        author = Author.query.filter(Author.name == name).first()
        author_id = author.id if author else -1
        cur = date.today()
        if Interactions.query.filter(Interactions.author_id == author_id
                                     and Interactions.recipe_id == recipe_id).count() > 0:
            interact = Interactions.query.filter(
                Interactions.author_id == author_id and Interactions.recipe_id == recipe_id).first()
            interact.rating = rating
            interact.created = cur
            DB.session.commit()
        else:
            DB.session.add(Interactions(rating=rating,
                                        author_id=author_id,
                                        recipe_id=recipe_id,
                                        created=cur))
            DB.session.commit()


def find_data_by_cuisine(search, cuisine):
    """ find recipe by cuisine """
    tmp = search
    if Note.query.filter(Note.cusine == cuisine).count() > 0:
        note = Note.query.filter(Note.cusine == cuisine).first()
        return note


def insert_recipe_data(data):
    """ insert data for recipe """
    if data:
        DB.session.bulk_insert_mappings(Note, data)
        DB.session.commit()


def delete_recipe_data(id_):
    """ insert data for recipe """
    if Note.query.filter(Note.id == id_).count() == 0:
        return False
    note = Note.query.filter(Note.id == id_).first()
    DB.session.delete(note)
    DB.session.commit()
    return True


def get_python_news(url):
    """ get python news """
    html = get_html(url)
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
