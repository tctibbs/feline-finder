"""Tracking-related use cases."""

from datetime import datetime

from loguru import logger

from src.entities import CatListing
from src.use_cases.cat_repository import CatRepository


def identify_new_cats(
    cat_repository: CatRepository, avalible_cat_listings: list[CatListing]
) -> list[CatListing]:
    """Identify new cats not already in the database."""
    existing_ids = {cat.cat_id for cat in cat_repository.list_cats()}
    logger.debug(f"Existing cat_ids in database: {len(existing_ids)}")

    new_cats = [
        listing
        for listing in avalible_cat_listings
        if listing.cat_id not in existing_ids
    ]

    logger.info(f"Identified {len(new_cats)} new cats.")
    for listing in new_cats:
        logger.debug(f"\tNew cat identified: {listing.cat_id} - {listing.name}")

    return new_cats


def identify_adopted_cats(
    cat_repository: CatRepository, available_cat_listings: list[CatListing]
) -> list[str]:
    """
    Identify cat_ids that were previously available but are now missing from the current listing,
    excluding cats already marked as 'Adopted'.
    """
    available_ids = {listing.cat_id for listing in available_cat_listings}
    tracked_cats = cat_repository.list_cats()

    adopted_ids = [
        cat.cat_id
        for cat in tracked_cats
        if cat.status != "Adopted" and cat.cat_id not in available_ids
    ]

    logger.info(
        f"Identified {len(adopted_ids)} cats that may have been adopted."
    )
    for cat_id in adopted_ids:
        logger.debug(f"\tAdopted cat identified: {cat_id}")

    return adopted_ids


def update_adoption_status(
    cat_repository: CatRepository, cat_id: str, status: str
) -> None:
    """Update a cat's adoption status and set date_adopted if applicable."""
    cat = cat_repository.get_cat_by_id(cat_id)
    if not cat:
        logger.warning(f"Cat with ID '{cat_id}' not found.")
        return

    cat.status = status

    if status.lower() == "adopted":
        cat.date_adopted = datetime.now()
        logger.info(f"Marked '{cat.name}' as adopted on {cat.date_adopted}.")

    cat_repository.save_cat(cat)  # new method you'll add to update full object
    logger.success(f"Updated status for '{cat.name}' to '{status}'.")
