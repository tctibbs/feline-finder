"""Feline Finder main script."""

import time
from pathlib import Path

import schedule
from loguru import logger

from source.alerts import DummyAlertSender, FilteredAlertSender
from source.alerts.usecases import filters
from source.monitoring import CatMonitor
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
    logger.info("Launching Feline Finder monitor...")

    # Initialize dependencies
    scraper = SafeHavenScraper()
    cat_repository = PolarsCatRepository(CAT_DB_PATH)
    image_repository = FilesystemImageRepository(IMAGE_DIR)

    # Create the monitoring orchestrator
    monitor = CatMonitor(
        listing_provider=scraper,
        cat_repo=cat_repository,
        image_repo=image_repository,
    )

    # Register alerts
    female_alert = FilteredAlertSender(DummyAlertSender())
    female_alert.add_filter(filters.is_female)
    monitor.register_alert(female_alert)

    # Run once at startup
    monitor.run_once()

    # Schedule every X minutes
    hour_interval = 2
    schedule.every(hour_interval).hours.do(monitor.run_once)
    logger.info(f"Monitoring scheduled every {hour_interval} hours.")

    # Event loop
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
