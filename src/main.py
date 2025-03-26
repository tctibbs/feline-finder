"""main.py"""

from loguru import logger

from src.infrastructure.cat_repository import PolarsCatRepository
from src.infrastructure.scrapers.safe_haven_scraper import SafeHavenScraper
from src.use_cases.scraping import (
    get_available_cat_listings,
    scrape_cat_details,
)
from src.use_cases.tracking import identify_new_cats

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
    database = PolarsCatRepository(
        "/workspaces/feline-finder/database/cats.parquet"
    )

    available_cat_listings = get_available_cat_listings(scraper)
    new_cat_listings = identify_new_cats(database, available_cat_listings)

    for listing in new_cat_listings:
        cat = scrape_cat_details(scraper, listing)
        if cat:
            cat.date_listed = listing.listing_date
            database.add_cat(cat)
            logger.success(f"Added '{cat.name}' to database.")
        else:
            logger.error(f"Failed scraping details for cat '{listing.cat_id}'.")

    logger.success("Workflow completed.")


if __name__ == "__main__":
    main()
