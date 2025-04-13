"""
Monitoring package for Feline Finder.

This package defines the functionality related to tracking
changes in cat availability and adoption status over time.
"""

from .usecases import tracking
from .adapters.cat_monitor import CatMonitor

__all__ = ["tracking", "CatMonitor"]
