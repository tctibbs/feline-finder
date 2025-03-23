"""Scraper for Safe Haven for Cats."""

from src.entities import Cat
from src.use_cases import CatScraper


class SafeHavenScraper(CatScraper):
    """Scraper for Safe Haven for Cats."""

    def get_available_cats(self) -> list[Cat]:
        return [
            Cat(name="Mittens", age="2 years", status="Available"),
            Cat(name="Shadow", age="4 months", status="Available"),
        ]
