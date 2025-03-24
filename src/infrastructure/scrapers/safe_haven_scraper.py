"""Scraper for Safe Haven for Cats."""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from loguru import logger

from src.entities import Cat
from src.use_cases import CatScraper

AVAILABLE_CATS_URL = "https://www.safehavenforcats.org"


class SafeHavenScraper(CatScraper):
    """Scraper for Safe Haven for Cats."""

    def get_available_cats(self) -> list[Cat]:
        listing_url = urljoin(AVAILABLE_CATS_URL, "/adopt/meet-the-cats/")
        logger.info(f"Fetching main cat listing from: {listing_url}")

        response = requests.get(listing_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        cat_cards = soup.find_all("div", class_="sme-card")
        logger.info(f"Found {len(cat_cards)} cat cards.")

        cats: list[Cat] = []

        for idx, card in enumerate(cat_cards, start=1):
            if idx > 2:
                break

            link = card.find("a", href=True)  # type: ignore
            if link is None:
                logger.warning(f"No link found for cat card #{idx}, skipping.")
                continue

            profile_url = urljoin(AVAILABLE_CATS_URL, link["href"])  # type: ignore
            cat = self._scrape_cat_profile(profile_url)

            if cat:
                logger.success(f"Successfully scraped '{cat.name}'.")
                cats.append(cat)
            else:
                logger.error(f"Failed to scrape cat at {profile_url}.")

        logger.info(f"Total cats scraped successfully: {len(cats)}")
        return cats

    def _scrape_cat_profile(self, url: str) -> Cat | None:
        logger.debug(f"Scraping cat profile from: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        name = self._extract_name(soup)
        image_urls = self._extract_images(soup)
        stats = self._extract_stats(soup)

        return Cat(
            name=name,
            age=stats.get("age", "Unknown"),
            gender=stats.get("gender", "Unknown"),
            breed=stats.get("breed", "Unknown"),
            color=stats.get("color", "Unknown"),
            declawed=stats.get("declawed?", "No") == "Yes",
            special_needs=stats.get("special needs?", "No") == "Yes",
            good_with_cats=self._parse_bool(stats.get("good with cats?")),
            good_with_dogs=self._parse_bool(stats.get("good with dogs?")),
            good_with_children=self._parse_bool(
                stats.get("good with children?")
            ),
            status="Available",
            story=self._extract_story(soup),
            image_urls=image_urls,
        )

    def _extract_name(self, soup: BeautifulSoup) -> str:
        intro_divs = soup.find_all("div", class_="et_pb_text_inner")
        name = "Unknown"
        for div in intro_divs:
            text = div.get_text(strip=True)
            if "Hey there!" in text:
                name_part = text.split("Hey there!", 1)[-1][4:]
                name = name_part.split("!")[0].strip()
                break
        logger.debug(f"Extracted name: '{name}'")
        return name

    def _extract_images(self, soup: BeautifulSoup) -> list[str]:
        image_tags = soup.find_all("img", class_="sme-round-small")
        images = [str(img.get("src")) for img in image_tags if img.get("src")]  # type: ignore
        logger.debug(f"Extracted {len(images)} images.")
        return images

    def _extract_stats(self, soup: BeautifulSoup) -> dict[str, str]:
        stats = {}
        table = soup.find("table", class_="sme-grid")
        if table:
            for row in table.find_all("tr", class_="sme-grid-row"):  # type: ignore
                cells = row.find_all("td", class_="sme-grid-cell")  # type: ignore
                if len(cells) == 2:
                    key = cells[0].text.strip().lower()
                    value = cells[1].text.strip()
                    stats[key] = value
        logger.debug("Extracted stats:")
        for key, value in stats.items():
            logger.debug(f"\t{key}: {value}")
        return stats

    def _extract_story(self, soup: BeautifulSoup) -> str | None:
        story_section = soup.find("div", class_="et_pb_text_5")
        story = story_section.get_text(strip=True) if story_section else None
        if story:
            logger.debug(f"Extracted story: {story[:30]}...")
        else:
            logger.debug("No story found.")
        return story

    def _parse_bool(self, val: str | None) -> bool | None:
        if val is None:
            return None
        return {"yes": True, "no": False}.get(val.lower(), None)
