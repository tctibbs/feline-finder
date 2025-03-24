"""Tracking-related use cases."""

from loguru import logger
from src.use_cases.cat_repository import CatRepository


def identify_new_cats(
    database: CatRepository, available_cats: dict[str, str]
) -> dict[str, str]:
    """Identify new cats not already in the database."""
    existing_names = {cat.name for cat in database.list_cats()}
    logger.debug(f"Existing cats in database: {len(existing_names)}")

    new_cats = {
        name: url
        for name, url in available_cats.items()
        if name not in existing_names
    }

    logger.info(f"Identified {len(new_cats)} new cats.")
    for cat_name in new_cats:
        logger.debug(f"\tNew cat identified: {cat_name}")

    return new_cats


def update_adoption_status(
    database: CatRepository, name: str, status: str
) -> None:
    """Update a cat's adoption status in the database."""
    logger.info(f"Updating status for '{name}' to '{status}'.")
    database.update_cat_status(name, status)
