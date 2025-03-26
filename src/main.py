"""main.py"""

from loguru import logger

from src.infrastructure.cat_repository import PolarsCatRepository
from src.infrastructure.scrapers.safe_haven_scraper import SafeHavenScraper
from src.use_cases import scraping, tracking
from pathlib import Path

# Configure Loguru logging format
logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<level>{message}</level>",
    colorize=True,
)


def main() -> None:
    logger.info("Starting workflow...")

    scraper = SafeHavenScraper()
    cat_repository = PolarsCatRepository(
        "/workspaces/feline-finder/database/cats.parquet"
    )

    # find current listings
    available_cat_listings = scraping.get_available_cat_listings(scraper)

    # Identify new cats
    new_cat_listings = tracking.identify_new_cats(
        cat_repository=cat_repository,
        avalible_cat_listings=available_cat_listings,
    )

    for listing in new_cat_listings:
        cat = scraping.scrape_cat_details(scraper, listing)
        if cat:
            cat_images = scraping.download_cat_images(cat)
            for image in cat_images:
                image.save(
                    Path("/workspaces/feline-finder/database/cat_images")
                    / f"{cat.date_listed}_{cat.cat_id}_{cat.name}_{cat.age}.png"
                )

            cat_repository.add_cat(cat)
            logger.success(f"Added '{cat.name}' to database.")
        else:
            logger.error(f"Failed scraping details for cat '{listing.cat_id}'.")

    # Identify adopted cats
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
