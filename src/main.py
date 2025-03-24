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

# List existing cats in the database
existing_cats = database.list_cats()
logger.info(f"Currently {len(existing_cats)} cats in the database.")
for cat in existing_cats:
    logger.debug(cat)

# Scrape available cats
cats = scraper.get_available_cats()

# Add scraped cats to the repository and print them
for cat in cats:
    if database.get_cat_by_name(cat.name):
        logger.info(f"{cat.name} already exists in database, skipping.")
        continue
    database.add_cat(cat)
    logger.success(f"Added {cat.name} to database.")
