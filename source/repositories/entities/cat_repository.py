"""Interface for Cat Repository."""

from abc import ABC, abstractmethod
from typing import List

from source.cat import Cat


class CatRepository(ABC):
    """Abstract interface for storing and retrieving cat records."""

    @abstractmethod
    def add_cat(self, cat: Cat) -> None:
        """Add a new cat to the repository."""

    @abstractmethod
    def get_cat_by_id(self, cat_id: str) -> Cat | None:
        """Retrieve a cat by unique ID."""

    @abstractmethod
    def get_cat_by_name(self, name: str) -> Cat | None:
        """Retrieve a cat by name."""

    @abstractmethod
    def save_cat(self, cat: Cat) -> None:
        """Replace or update an entire cat record."""

    @abstractmethod
    def update_cat_status(self, cat_id: str, status: str) -> None:
        """Update the adoption status of a cat by ID."""

    @abstractmethod
    def list_cats(self, status: str | None = None) -> List[Cat]:
        """List all cats, optionally filtered by status."""
