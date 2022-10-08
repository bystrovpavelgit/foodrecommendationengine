"""web util"""
import requests
from requests import ReadTimeout, ConnectTimeout, Timeout
from requests.exceptions import HTTPError


def get_html(link):
    """ get html function"""
    try:
        result = requests.get(link, timeout=8.0)
        result.raise_for_status()
        return result.text
    except (HTTPError, ConnectTimeout, ReadTimeout, Timeout, ConnectionError):
        print("connection ошибка")
    except(requests.RequestException, ValueError):
        print('ошибка')
    return False
