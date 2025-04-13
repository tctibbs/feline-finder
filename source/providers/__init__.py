"""
Cat listing providers for the Feline Finder application.

This package defines the domain logic and concrete implementations for
external data sources that provide adoptable cat listings.
"""

from .entities.cat_provider import CatListingProvider
from .infrastructure.safe_haven_scraper import SafeHavenScraper

__all__ = ["CatListingProvider", "SafeHavenScraper"]
