"""Abstract interface for cat scrapers."""

from abc import ABC, abstractmethod
from typing import List
from src.entities import Cat


class CatScraper(ABC):
    """Abstract interface for cat scrapers."""

    @abstractmethod
    def get_available_cats(self) -> List[Cat]:
        """Scrape and return a list of currently available cats."""
        pass
