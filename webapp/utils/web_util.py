"""
    Apache License 2.0 Copyright (c) 2022 Pavel Bystrov
    web util
"""
from bs4 import BeautifulSoup
import logging
import requests
from requests import ReadTimeout, ConnectTimeout, Timeout
from requests.exceptions import HTTPError

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/20100101 Firefox/65.0'
    }


def get_html(link):
    """ get html function"""
    try:
        result = requests.get(link, headers=headers, timeout=8.0)
        result.raise_for_status()
        return result.text
    except (HTTPError, ConnectTimeout, ReadTimeout, Timeout, ConnectionError):
        logging.error("ошибка ConnectTimeout или HTTP ошибка в функции get_html")
    except(requests.RequestException, ValueError):
        logging.error("ошибки RequestException или ValueError в функции get_html")
    return False


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
