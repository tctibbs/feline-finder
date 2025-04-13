"""
Alerting package for notifying users when new cats are discovered.
"""

from .entities.cat_alert_sender import CatAlertSender
from .usecases.filtered_alert_sender import FilteredAlertSender
from .usecases import filters
from .infrastructure.dummy_alert_sender import DummyAlertSender

__all__ = [
    "CatAlertSender",
    "FilteredAlertSender",
    "filters",
    "DummyAlertSender",
]
