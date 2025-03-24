"""Scraping-related use cases."""

from src.entities import Cat
from src.use_cases import CatScraper
from typing import Dict


def get_available_cats(scraper: CatScraper) -> Dict[str, str]:
    """Retrieve available cat listings (name to URL mapping)."""
    return scraper.get_available_listings()


def scrape_cat_details(scraper: CatScraper, url: str) -> Cat | None:
    """Scrape detailed cat information from a cat profile URL."""
    return scraper.scrape_cat_profile(url)
