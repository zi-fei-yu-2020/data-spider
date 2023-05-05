import requests

from .exceptions import FetchError
import urllib3

urllib3.disable_warnings()


class Fetcher:
    def __init__(self):
        pass

    def fetch(self, url):
        try:
            headers = {'Accept-Encoding': 'gzip, deflate, br'}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except Exception as e:
            raise FetchError(f"Failed to fetch {url}: {e}")
