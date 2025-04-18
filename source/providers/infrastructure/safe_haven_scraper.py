"""Scraper for Safe Haven for Cats."""

from datetime import datetime
from io import BytesIO
from urllib.parse import parse_qs, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from loguru import logger
from PIL import Image

from source.cat import Cat, CatListing

from .. import CatListingProvider

AVAILABLE_CATS_URL = "https://www.safehavenforcats.org"


class SafeHavenScraper(CatListingProvider):
    """Scraper for Safe Haven for Cats."""

    def get_available_listings(self) -> list[CatListing]:
        """Scrape and return a list of currently available CatListings."""
        listing_url = urljoin(AVAILABLE_CATS_URL, "/adopt/meet-the-cats/")
        logger.info(f"Fetching main cat listing from: {listing_url}")

        response = requests.get(listing_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        cat_cards = soup.find_all("div", class_="sme-card")

        now = datetime.now()
        listings: list[CatListing] = []
        seen_ids: set[str] = set()

        for card in cat_cards:
            name_tag = card.find("h5", class_="sme-anm-name")  # type: ignore
            if not name_tag:
                logger.warning("Cat name not found in card, skipping.")
                continue

            link = name_tag.find("a", href=True)  # type: ignore
            if not link:
                logger.warning(
                    "Profile URL not found in cat name tag, skipping."
                )
                continue

            profile_url = link["href"]  # type: ignore
            cat_id = self._extract_cat_id(profile_url)  # type: ignore
            if not cat_id or cat_id in seen_ids:
                continue

            seen_ids.add(cat_id)

            listings.append(
                CatListing(
                    cat_id=cat_id,
                    name=link.text.strip(),
                    url=profile_url,  # type: ignore
                    listing_date=now,
                )
            )

        logger.info(f"Total cats available for adoption: {len(listings)}")
        return listings

    def get_cat_profile(self, listing: CatListing) -> Cat | None:
        """Scrape a full Cat profile based on a CatListing."""
        return self._scrape_from_url(listing)

    def get_cat_images(self, cat: Cat) -> list[Image.Image]:
        """
        Downloads and returns the cat's images as a list of PIL Images.

        Skips any images that fail to download or parse.
        """
        if not cat.image_urls:
            logger.warning(f"No image URLs found for cat '{cat.name}'.")
            return []

        images: list[Image.Image] = []

        for url in cat.image_urls:
            try:
                logger.debug(f"Downloading image: {url}")
                response = requests.get(str(url), timeout=10)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content)).convert("RGB")
                images.append(image)
            except (requests.RequestException, IOError) as e:
                logger.warning(f"Failed to download image from {url}: {e}")

        logger.info(f"Downloaded {len(images)} images for '{cat.name}'")
        return images

    def _scrape_from_url(self, listing: CatListing) -> Cat | None:
        url = listing.url
        logger.debug(f"Scraping cat profile from: {url}")

        try:
            response = requests.get(str(url))
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        image_urls = self._extract_images(soup)
        stats = self._extract_stats(soup)

        cat = Cat(
            cat_id=listing.cat_id,
            name=listing.name,
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
            image_urls=[urljoin(AVAILABLE_CATS_URL, src) for src in image_urls],  # type: ignore
            shelter="Safe Haven for Cats",
            date_listed=listing.listing_date,
            date_adopted=None,
        )

        return cat

    def _extract_cat_id(self, url: str) -> str | None:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        return qs.get("animal_id", [None])[0]

    def _extract_images(self, soup: BeautifulSoup) -> list[str]:
        image_tags = soup.find_all("img", class_="sme-round-small")
        images = [img["src"] for img in image_tags if img.get("src")]  # type: ignore
        logger.debug(f"Extracted {len(images)} images.")
        return images  # type: ignore

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
