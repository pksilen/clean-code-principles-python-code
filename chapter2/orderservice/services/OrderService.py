from typing import Protocol

from ..dtos.InputOrder import InputOrder
from ..dtos.OutputOrder import OutputOrder


class OrderService(Protocol):
    def create_order(self, input_order: InputOrder) -> OutputOrder:
        pass

    def get_order(self, id_: str) -> OutputOrder:
        pass
