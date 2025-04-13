"""Cat image repository interface."""

from abc import ABC, abstractmethod

from PIL import Image

from source.cat import Cat


class CatImageRepository(ABC):
    """Abstract interface for storing cat image data."""

    @abstractmethod
    def save_images(self, cat: Cat, images: list[Image.Image]) -> None:
        """
        Save the provided PIL images associated with a cat to storage.
        """
