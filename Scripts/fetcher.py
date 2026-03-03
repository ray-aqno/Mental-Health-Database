import requests
import time


class Fetcher:
    def __init__(self, session=None, rate_limit_seconds=1):
        self.session = session or requests.Session()
        self.rate_limit_seconds = rate_limit_seconds

    def fetch(self, url, timeout=15):
        try:
            resp = self.session.get(url, timeout=timeout)
            resp.raise_for_status()
            time.sleep(self.rate_limit_seconds)
            return resp
        except Exception:
            return None
