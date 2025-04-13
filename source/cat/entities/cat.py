"""Cat data model."""

from datetime import datetime

from pydantic import BaseModel, HttpUrl


class Cat(BaseModel):
    """Encapsulates information pertaining to a cat listing."""

    cat_id: str
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
    image_urls: list[HttpUrl] | None = None
    shelter: str
    date_listed: datetime
    date_adopted: datetime | None = None

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.age}, {self.gender}, {self.breed})"
            f" - {self.status}"
        )
