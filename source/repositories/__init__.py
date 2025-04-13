"""
Repository package for Feline Finder.

This package defines how cat-related data is stored and retrieved.
"""

from .entities.cat_repository import CatRepository
from .infrastructure.cat_repository_polars import PolarsCatRepository

__all__ = ["CatRepository", "PolarsCatRepository"]
