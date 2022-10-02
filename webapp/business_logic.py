"""business logic"""
from bs4 import BeautifulSoup
import requests


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



