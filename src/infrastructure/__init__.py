"""
Infrastructure package.

This package contains concrete implementations of abstract interfaces defined in
inner layers of the application.
"""

from . import scrapers, cat_repository

__all__ = ["scrapers", "cat_repository"]
