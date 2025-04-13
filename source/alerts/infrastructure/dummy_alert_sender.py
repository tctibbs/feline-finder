"""Dummy sender for new cat alerts."""

from loguru import logger

from source.cat import Cat

from .. import CatAlertSender


class DummyAlertSender(CatAlertSender):
    """Dummy alert sender for testing purposes."""

    def send(self, cat: Cat) -> None:
        """Log an alert instead of sending a real one."""
        if not self.should_send(cat):
            logger.debug(
                f"[DummyAlert] Skipped alert for {cat.name} (filtered out)"
            )
            return

        logger.info(
            f"[Dummy Alert] New cat found: {cat.name} (ID: {cat.cat_id})"
        )
