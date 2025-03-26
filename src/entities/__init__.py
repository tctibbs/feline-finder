"""
Entities package.

This package contains the core domain models of the application.

In Clean Architecture, entities are the most stable and reusable components.
They should not depend on any other layer of the application.
"""

from .cat import Cat, CatListing

__all__ = ["Cat", "CatListing"]
