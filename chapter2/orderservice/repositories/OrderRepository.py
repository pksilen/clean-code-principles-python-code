from typing import Protocol

from ..entities.Order import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> None:
        pass

    def find(self, id_: str) -> Order | None:
        pass

    # Rest of methods...
