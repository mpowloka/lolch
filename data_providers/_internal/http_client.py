import requests
import time
from .errors import RiotAPIError

class HttpClient:
    def __init__(self, max_retries: int = 3, backoff: float = 1.0):
        self.max_retries = max_retries
        self.backoff = backoff

    def get(self, url: str, headers: dict = None, timeout: float = 5.0):
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    time.sleep(self.backoff * (attempt + 1))
                else:
                    raise RiotAPIError(f"Error {response.status_code}: {response.text}")
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise RiotAPIError(f"Failed GET {url}: {e}")
                time.sleep(self.backoff * (attempt + 1))