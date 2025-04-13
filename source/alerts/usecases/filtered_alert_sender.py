"""Filtered alert sender."""

from collections.abc import Callable

from source.cat import Cat

from .. import CatAlertSender


class FilteredAlertSender(CatAlertSender):
    """Wraps an alert sender and only forwards if filters pass."""

    def __init__(
        self,
        sender: CatAlertSender,
        filters: list[Callable[[Cat], bool]] | None = None,
    ) -> None:
        self.sender = sender
        self.filters = filters or []

    def add_filter(self, f: Callable[[Cat], bool]) -> None:
        self.filters.append(f)

    def send(self, cat: Cat) -> None:
        if all(f(cat) for f in self.filters):
            self.sender.send(cat)
