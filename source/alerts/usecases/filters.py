"""Reusable filters for alerting on cats."""

from collections.abc import Callable

from source.cat import Cat


def is_female(cat: Cat) -> bool:
    """Return True if the cat is female."""
    return cat.gender.lower() == "female"


def is_male(cat: Cat) -> bool:
    """Return True if the cat is male."""
    return cat.gender.lower() == "male"


def breed_contains(substring: str) -> Callable[[Cat], bool]:
    """Return True if the breed contains the given substring."""
    return lambda cat: substring.lower() in cat.breed.lower()


def color_is(color_name: str) -> Callable[[Cat], bool]:
    """Return True if the color matches the given value."""
    return lambda cat: color_name.lower() in cat.color.lower()


def not_declawed(cat: Cat) -> bool:
    """Return True if the cat is not declawed."""
    return not cat.declawed
