"""CatMonitor adapter for orchestrating periodic monitoring of cat listings."""

from loguru import logger

from source.alerts import CatAlertSender
from source.monitoring import tracking
from source.providers import CatListingProvider
from source.repositories import CatImageRepository, CatRepository


class CatMonitor:
    """Adapter that orchestrates periodic monitoring of cat listings."""

    def __init__(
        self,
        listing_provider: CatListingProvider,
        cat_repo: CatRepository,
        image_repo: CatImageRepository,
    ) -> None:
        self.provider = listing_provider
        self.cat_repo = cat_repo
        self.image_repo = image_repo
        self._alerts: list[CatAlertSender] = []

    def register_alert(self, alert: CatAlertSender) -> None:
        """Register a CatAlertSender to be notified of new cats."""
        self._alerts.append(alert)

    def run_once(self) -> None:
        logger.info("🐾 Running CatMonitor workflow...")

        listings = self.provider.get_available_listings()

        new_cats = tracking.identify_new_cats(self.cat_repo, listings)
        for listing in new_cats:
            cat = self.provider.get_cat_profile(listing)
            if not cat:
                logger.error(f"Failed to fetch cat {listing.cat_id}")
                continue

            images = self.provider.get_cat_images(cat)
            self.image_repo.save_images(cat, images)
            self.cat_repo.add_cat(cat)
            logger.success(f"Added new cat '{cat.name}'")

            for alert in self._alerts:
                alert.send(cat)

        adopted_ids = tracking.identify_adopted_cats(self.cat_repo, listings)
        for cat_id in adopted_ids:
            tracking.update_adoption_status(self.cat_repo, cat_id, "Adopted")

        logger.info("✅ CatMonitor cycle complete.")
