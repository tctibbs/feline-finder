"""
Repository package for Feline Finder.

This package defines how cat-related data is stored and retrieved.
"""

from .entities.cat_repository import CatRepository
from .entities.cat_image_repository import CatImageRepository
from .infrastructure.cat_repository_polars import PolarsCatRepository
from .infrastructure.filesystem_image_repository import (
    FilesystemImageRepository,
)

__all__ = [
    "CatRepository",
    "CatImageRepository",
    "PolarsCatRepository",
    "FilesystemImageRepository",
]
