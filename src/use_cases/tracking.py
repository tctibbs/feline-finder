"""Tracking-related use cases."""

from loguru import logger

from src.entities import CatListing
from src.use_cases.cat_repository import CatRepository


def identify_new_cats(
    database: CatRepository, available_cats: list[CatListing]
) -> list[CatListing]:
    """Identify new cats not already in the database."""
    existing_ids = {cat.cat_id for cat in database.list_cats()}
    logger.debug(f"Existing cat_ids in database: {len(existing_ids)}")

    new_cats = [
        listing
        for listing in available_cats
        if listing.cat_id not in existing_ids
    ]

    logger.info(f"Identified {len(new_cats)} new cats.")
    for listing in new_cats:
        logger.debug(f"\tNew cat identified: {listing.cat_id} - {listing.name}")

    return new_cats


def update_adoption_status(
    database: CatRepository, name: str, status: str
) -> None:
    """Update a cat's adoption status in the database."""
    logger.info(f"Updating status for '{name}' to '{status}'.")
    database.update_cat_status(name, status)
