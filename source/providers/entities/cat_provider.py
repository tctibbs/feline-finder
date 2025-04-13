"""Abstract interface for cat listing providers."""

from abc import ABC, abstractmethod

from PIL import Image

from source.cat import Cat, CatListing


class CatListingProvider(ABC):
    """
    Abstract interface for providers of adoptable cat listings.
    """

    @abstractmethod
    def get_available_listings(self) -> list[CatListing]:
        """
        Return a list of currently available cat listings.
        """
        pass

    @abstractmethod
    def get_cat_profile(self, listing: CatListing) -> Cat | None:
        """
        Given a CatListing, return the full Cat profile.
        Returns None if the profile could not be retrieved.
        """
        pass

    @abstractmethod
    def get_cat_images(self, cat: Cat) -> list[Image.Image]:
        """
        Given a Cat, return a list of images of that cat.
        """
        pass
