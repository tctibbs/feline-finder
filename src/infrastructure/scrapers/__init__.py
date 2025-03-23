"""
Scrapers subpackage.

This package contains concrete implementations of `CatScraper` interfaces
defined in the `use_cases` layer. Each scraper knows how to extract and
normalize data from a specific external source or shelter.
"""

from .safe_haven_scraper import SafeHavenScraper

__all__ = [
    "SafeHavenScraper",
]
