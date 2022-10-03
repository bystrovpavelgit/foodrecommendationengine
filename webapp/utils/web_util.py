"""web util"""
import requests
from requests import ReadTimeout, ConnectTimeout, Timeout


def get_html(link):
    """ get html function"""
    try:
        result = requests.get(link, timeout=8.0)
        result.raise_for_status()
        return result.text
    except (ConnectTimeout, ReadTimeout, Timeout, ConnectionError):
        print("connection error")
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
    return False
