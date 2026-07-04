from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
import logging

providers_logger = logging.getLogger("providers")


class BaseProvider(ABC):
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
    
    @abstractmethod
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        pass
    
    def get_page(self, url: str) -> BeautifulSoup:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            providers_logger.info(f"Fetched page: {url}")
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            providers_logger.error(f"Error fetching {url}: {str(e)}")
            return None