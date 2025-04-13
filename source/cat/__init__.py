"""
Cat package.

This package defines the core domain model for adoptable cats.
"""

from .entities.cat import Cat
from .entities.cat_listing import CatListing

__all__ = ["Cat", "CatListing"]
