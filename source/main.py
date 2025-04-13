"""Feline Finder main script."""

from pathlib import Path

from loguru import logger

from source.monitoring import tracking
from source.providers import SafeHavenScraper
from source.repositories import FilesystemImageRepository, PolarsCatRepository

# Configure Loguru logging format
logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<level>{message}</level>",
    colorize=True,
)

CAT_DB_PATH = Path("/workspaces/feline-finder/database/cats.parquet")
IMAGE_DIR = Path("/workspaces/feline-finder/database/cat_images")


def main() -> None:
    logger.info("Starting workflow...")

    scraper = SafeHavenScraper()
    cat_repository = PolarsCatRepository(CAT_DB_PATH)
    image_repository = FilesystemImageRepository(IMAGE_DIR)

    # Get current cat listings from providers
    available_cat_listings = scraper.get_available_listings()

    # Identify new cats not in the repository
    new_cat_listings = tracking.identify_new_cats(
        cat_repository=cat_repository,
        avalible_cat_listings=available_cat_listings,
    )

    for listing in new_cat_listings:
        cat = scraper.get_cat_profile(listing)

        if not cat:
            logger.error(f"Failed scraping details for cat '{listing.cat_id}'.")
            continue

        cat_images = scraper.get_cat_images(cat)
        image_repository.save_images(cat, cat_images)
        cat_repository.add_cat(cat)
        logger.success(f"Added '{cat.name}' to database.")

    # Identify cats that have likely been adopted
    adopted_cat_ids = tracking.identify_adopted_cats(
        cat_repository=cat_repository,
        available_cat_listings=available_cat_listings,
    )

    for cat_id in adopted_cat_ids:
        tracking.update_adoption_status(
            cat_repository=cat_repository,
            cat_id=cat_id,
            status="Adopted",
        )

    logger.success("Workflow completed.")


if __name__ == "__main__":
    main()
