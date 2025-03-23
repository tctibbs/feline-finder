"""Cat data model."""

from dataclasses import dataclass


@dataclass
class Cat:
    """Encapsulates information pertaining to a cat listing."""

    name: str
    age: str
    gender: str
    breed: str
    color: str
    declawed: bool
    special_needs: bool
    good_with_cats: bool | None
    good_with_dogs: bool | None
    good_with_children: bool | None
    status: str
    story: str | None = None
    image_urls: list[str] | None = None

    def __str__(self) -> str:
        return f"{self.name} ({self.age}, {self.gender}, {self.breed}) - {self.status}"
