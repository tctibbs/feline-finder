"""Cat alert sender interface."""

from abc import ABC, abstractmethod

from source.cat import Cat


class CatAlertSender(ABC):
    """Abstract adapter for sending alerts when a new cat is found."""

    @abstractmethod
    def send(self, cat: Cat) -> None:
        """Send an alert for the given cat."""
