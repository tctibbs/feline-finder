"""Module containing Cat entity."""

from dataclasses import dataclass


@dataclass
class Cat:
    """Encapsulates the information pertaining to a cat."""

    name: str
    age: str
    status: str
