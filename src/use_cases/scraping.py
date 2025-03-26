"""Scraping-related use cases."""

from src.entities import Cat, CatListing
from src.use_cases import CatScraper


def get_available_cat_listings(scraper: CatScraper) -> list[CatListing]:
    """Retrieve available cat listings."""
    return scraper.get_available_listings()


def scrape_cat_details(scraper: CatScraper, listing: CatListing) -> Cat | None:
    """Scrape detailed cat information from a cat profile URL."""
    return scraper.scrape_cat_listing(listing)
