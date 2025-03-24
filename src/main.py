"""main.py"""

from loguru import logger

from src.infrastructure.cat_repository import PolarsCatRepository
from src.infrastructure.scrapers.safe_haven_scraper import SafeHavenScraper
from src.use_cases.scraping import get_available_cats, scrape_cat_details
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

    available_cats = get_available_cats(scraper)
    new_cats = identify_new_cats(database, available_cats)

    for name, profile_url in new_cats.items():
        cat = scrape_cat_details(scraper, profile_url)
        if cat:
            database.add_cat(cat)
        else:
            logger.error(f"Failed scraping details for cat '{name}'.")

    logger.success("Workflow completed.")


if __name__ == "__main__":
    main()
