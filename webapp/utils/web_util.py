"""web util"""
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
        print("connection or HTTP error")
    except(requests.RequestException, ValueError):
        print('ошибка')
    return False
