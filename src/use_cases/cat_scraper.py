"""Abstract interface for cat scrapers."""

from abc import ABC, abstractmethod

from src.entities.cat import Cat, CatListing


class CatScraper(ABC):
    """Abstract interface for cat scrapers."""

    @abstractmethod
    def get_available_listings(self) -> list[CatListing]:
        """
        Scrape and return a list of currently available cat listings.
        """
        pass

    @abstractmethod
    def scrape_cat_listing(self, listing: CatListing) -> Cat | None:
        """
        Given a CatListing, scrape and return the full Cat profile.
        """
        pass
