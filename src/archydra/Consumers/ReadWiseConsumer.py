from archydra.AbstractClasses import Consumer
from urllib.parse import urlparse
import requests
from loguru import logger

class ReadWiseConsumer(Consumer):
    def test_token(self):
        parsed = urlparse(self.rw_endpoint)
        new_url = f"{parsed.scheme}://{parsed.netloc}/api/v2/auth"
        logger.debug("Testing token on {}",new_url)
        response = self.session.get(new_url)
        if response.status_code != 204:
            logger.error("API Token test failed: {}",response)
            return False
        logger.success("Successfully authenticated to ReadWise API!")
        return True

    def __init__(self, api_token:str, rw_endpoint="https://readwise.io/api/v3", test_token=True):
        self.session = requests.Session()
        self.session.headers.update({"Authorization":f"Token {api_token}"})
        self.rw_endpoint = rw_endpoint
        if test_token:
            try:
                token_okay = self.test_token()
            except requests.exceptions.HTTPError as e:
                logger.error("Your API Token is invalid")
                raise e
            if not token_okay:
                raise Exception("Readwise Token is bad")
        super().__init__()

    def process_url(self, url):
        logger.info("Sending url: {} to readwise...",url)
        response = self.session.post(f"{self.rw_endpoint}/save",
                          json={
                              "url":url
                          })
        response.raise_for_status()
        if response.status_code == 200:
            logger.warning("url {} was already in readwise...", url)
        logger.trace("Readwise response: {}",response.json())
        return super().process_url(url)
