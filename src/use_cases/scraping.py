"""Scraping-related use cases."""

from io import BytesIO

import requests
from loguru import logger
from PIL import Image

from src.entities import Cat, CatListing
from src.use_cases import CatScraper


def get_available_cat_listings(scraper: CatScraper) -> list[CatListing]:
    """Retrieve available cat listings."""
    return scraper.get_available_listings()


def scrape_cat_details(scraper: CatScraper, listing: CatListing) -> Cat | None:
    """Scrape detailed cat information from a cat profile URL."""
    return scraper.scrape_cat_listing(listing)


def download_cat_images(cat: Cat) -> list[Image.Image]:
    """
    Download and return the cat's images as a list of PIL Images.

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
        except Exception as e:
            logger.warning(f"Failed to download image from {url}: {e}")

    logger.info(f"Downloaded {len(images)} images for '{cat.name}'")
    return images
