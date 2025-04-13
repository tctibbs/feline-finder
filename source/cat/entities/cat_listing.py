"""Cat Listing model."""

from datetime import datetime

from pydantic import BaseModel, HttpUrl


class CatListing(BaseModel):
    """Information about a cat being listed as available."""

    cat_id: str
    name: str
    url: HttpUrl
    listing_date: datetime
