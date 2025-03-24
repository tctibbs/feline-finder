"""Main Module."""

from loguru import logger

import src

# Configure Loguru logging format
logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<level>{message}</level>",
    colorize=True,
)

# Initialize the cat repository using Parquet format
database = src.infrastructure.cat_repository.PolarsCatRepository(
    "/workspaces/feline-finder/database/cats.parquet"
)

# Initialize the scraper for Safe Haven for Cats
scraper = src.infrastructure.scrapers.SafeHavenScraper()

# Check available cats
available_cats = scraper.get_available_listings()

# Get existing cats from database
existing_cats = database.list_cats()
logger.info(f"Currently {len(existing_cats)} cats in database.")
for cat in existing_cats:
    logger.debug(f"\t{cat}")

# Identify cats needing scraping
cats_to_scrape = {
    name: url
    for name, url in available_cats.items()
    if name not in [cat.name for cat in existing_cats]
}
logger.info(f"{len(cats_to_scrape)} new cats to scrape.")

# Scrape and add new cats to database
for cat_name, profile_url in cats_to_scrape.items():
    cat = scraper.scrape_cat_profile(profile_url)
    if cat:
        database.add_cat(cat)
        logger.success(f"Added '{cat.name}' to database.")
    else:
        logger.error(f"Failed to scrape '{cat_name}'.")
