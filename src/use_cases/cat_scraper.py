"""Abstract interface for cat scrapers."""

from abc import ABC, abstractmethod

from src.entities.cat import Cat


class CatScraper(ABC):
    """Abstract interface for cat scrapers."""

    @abstractmethod
    def get_available_listings(self) -> dict[str, str]:
        """
        Scrape and return a list of currently available
        cats by name and profile URL.
        """
        pass

    @abstractmethod
    def scrape_cat_profile(self, profile_url: str) -> Cat | None:
        """
        Given a cat's profile URL, scrape detailed information
        and return a Cat object.
        """
        pass
