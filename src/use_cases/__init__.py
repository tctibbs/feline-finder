"""
Use Cases package.

This package contains the application-specific business rules and orchestration
logic, as well as any abstract interfaces needed to fulfill those use cases.
"""

from .cat_scraper import CatScraper

__all__ = ["CatScraper"]
