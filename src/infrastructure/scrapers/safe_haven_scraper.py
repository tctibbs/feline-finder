"""Scraper for Safe Haven for Cats."""

from src.entities import Cat
from src.use_cases import CatScraper


class SafeHavenScraper(CatScraper):
    """Scraper for Safe Haven for Cats."""

    def get_available_cats(self) -> list[Cat]:
        return [
            Cat(
                name="Mittens",
                age="2 years",
                gender="Female",
                breed="Domestic Short Hair",
                color="Black",
                declawed=False,
                special_needs=False,
                good_with_cats=None,
                good_with_dogs=None,
                good_with_children=None,
                status="Available",
                story=None,
                image_urls=[],
            ),
            Cat(
                name="Shadow",
                age="4 months",
                gender="Male",
                breed="Tabby",
                color="Gray",
                declawed=False,
                special_needs=False,
                good_with_cats=None,
                good_with_dogs=None,
                good_with_children=None,
                status="Available",
                story=None,
                image_urls=[],
            ),
        ]
