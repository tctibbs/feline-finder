"""
Alerting package for notifying users when new cats are discovered.
"""

from .entities.cat_alert_sender import CatAlertSender
from .infrastructure.dummy_alert_sender import DummyAlertSender

__all__ = ["CatAlertSender", "DummyAlertSender"]
