"""Interface for Cat Repository."""

from abc import ABC, abstractmethod
from typing import List
from src.entities import Cat


class CatRepository(ABC):
    """Abstract interface for a cat repository."""

    @abstractmethod
    def add_cat(self, cat: Cat) -> None:
        """Add a new cat to the repository."""

    @abstractmethod
    def get_cat_by_name(self, name: str) -> Cat | None:
        """Retrieve a cat by name."""

    @abstractmethod
    def update_cat_status(self, name: str, status: str) -> None:
        """Update the adoption status of a cat."""

    @abstractmethod
    def list_cats(self, status: str | None = None) -> List[Cat]:
        """List all cats, optionally filtered by status."""
