from archydra.Abstracts import Consumer
from urllib.parse import urlparse, urlunparse
import requests

class ReadWiseConsumer(Consumer):
    def test_token(self):
        parsed = urlparse(self.rw_endpoint)
        new_url = f"{parsed.scheme}://{parsed.netloc}/api/v2/auth"
        response = self.session.get(new_url)
        response.raise_for_status()
        return response

    def __init__(self, api_token:str, rw_endpoint="https://readwise.io/api/v3", test_token=True):
        self.session = requests.Session()
        self.session.headers.update({"Authorization":f"Token {api_token}"})
        self.rw_endpoint = rw_endpoint
        if test_token:
            try:
                self.test_token()
            except requests.exceptions.HTTPError:
                print("Your API Token is invalid")
                raise Exception
        super().__init__()

    def process_url(self, url):
        response = self.session.post(f"{self.rw_endpoint}/save",
                          json={
                              "url":url
                          })
        response.raise_for_status()
        return super().process_url(url)

