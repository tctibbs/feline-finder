"""Polars implementation of CatRepository using Parquet."""

from pathlib import Path
from typing import List

import polars as pl

from source.cat import Cat

from .. import CatRepository


class PolarsCatRepository(CatRepository):
    """Polars-based cat repository implementation using Parquet."""

    def __init__(self, parquet_path: Path) -> None:
        self.parquet_path = parquet_path
        if not parquet_path.exists():
            raise FileNotFoundError(f"Parquet file not found: {parquet_path}")
        try:
            self.df = pl.read_parquet(parquet_path)
        except FileNotFoundError:
            self.df = pl.DataFrame(
                schema={
                    "cat_id": pl.Utf8,
                    "name": pl.Utf8,
                    "age": pl.Utf8,
                    "gender": pl.Utf8,
                    "breed": pl.Utf8,
                    "color": pl.Utf8,
                    "declawed": pl.Boolean,
                    "special_needs": pl.Boolean,
                    "good_with_cats": pl.Boolean,
                    "good_with_dogs": pl.Boolean,
                    "good_with_children": pl.Boolean,
                    "status": pl.Utf8,
                    "story": pl.Utf8,
                    "image_urls": pl.List(pl.Utf8),
                    "shelter": pl.Utf8,
                    "date_listed": pl.Datetime,
                    "date_adopted": pl.Datetime,
                }
            )
            self._save()

    def _save(self) -> None:
        """Save current state to Parquet."""
        self.df.write_parquet(self.parquet_path)

    def add_cat(self, cat: Cat) -> None:
        """Add a new cat to the repository."""
        new_row = pl.DataFrame(
            {
                "cat_id": [cat.cat_id],
                "name": [cat.name],
                "age": [cat.age],
                "gender": [cat.gender],
                "breed": [cat.breed],
                "color": [cat.color],
                "declawed": [cat.declawed],
                "special_needs": [cat.special_needs],
                "good_with_cats": [cat.good_with_cats],
                "good_with_dogs": [cat.good_with_dogs],
                "good_with_children": [cat.good_with_children],
                "status": [cat.status],
                "story": [cat.story],
                "image_urls": [[str(url) for url in (cat.image_urls or [])]],
                "shelter": [cat.shelter],
                "date_listed": [cat.date_listed],
                "date_adopted": [cat.date_adopted],
            },
        )
        self.df = pl.concat([self.df, new_row], how="vertical")
        self._save()

    def get_cat_by_name(self, name: str) -> Cat | None:
        """Retrieve a cat by name."""
        result = self.df.filter(pl.col("name") == name)
        if result.is_empty():
            return None
        data = result.to_dicts()[0]
        return Cat(**data)

    def get_cat_by_id(self, cat_id: str) -> Cat | None:
        """Retrieve a cat by unique ID."""
        result = self.df.filter(pl.col("cat_id") == cat_id)
        if result.is_empty():
            return None
        return Cat(**result.to_dicts()[0])

    def update_cat_status(self, cat_id: str, status: str) -> None:
        """Update only the status field of a cat by ID."""
        self.df = self.df.with_columns(
            pl.when(pl.col("cat_id") == cat_id)
            .then(status)
            .otherwise(pl.col("status"))
            .alias("status")
        )
        self._save()

    def save_cat(self, cat: Cat) -> None:
        """Update a cat record by replacing it entirely."""
        self.df = self.df.filter(pl.col("cat_id") != cat.cat_id)
        self.add_cat(cat)
        self._save()

    def list_cats(self, status: str | None = None) -> List[Cat]:
        """List all cats, optionally filtered by status."""
        result = (
            self.df
            if status is None
            else self.df.filter(pl.col("status") == status)
        )
        return [Cat(**row) for row in result.to_dicts()]
