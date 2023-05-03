import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple
from .exceptions import FetchError
import urllib3
urllib3.disable_warnings()

class Rule:
    def __init__(self, rule: Dict[str, List[Tuple[str, str]]]):
        self.rule = rule
        self.fetcher = Fetcher()

    def parse(self, response: str) -> Dict[str, List[str]]:
        soup = BeautifulSoup(response, 'html.parser')
        parsed_data = {}
        for key, tags in self.rule.items():
            parsed_data[key] = []
            for tag_name, class_name in tags:
                tags = soup.find_all(tag_name, class_=class_name)
                parsed_data[key].extend([tag.text for tag in tags])
        return parsed_data

class Fetcher:
    def fetch(self, url):
        try:
            headers = {'Accept-Encoding': 'gzip, deflate, br'}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except Exception as e:
            raise FetchError(f"Failed to fetch {url}: {e}")
