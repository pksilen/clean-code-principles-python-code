from typing import Protocol

from ..dtos.InputOrder import InputOrder
from ..entities.Order import Order


class OrderRepository(Protocol):
    def initialize(self) -> None:
        pass

    def save(self, order: InputOrder) -> Order:
        pass

    def find(self, order_id: int) -> Order | None:
        pass

    # Rest of methods...
