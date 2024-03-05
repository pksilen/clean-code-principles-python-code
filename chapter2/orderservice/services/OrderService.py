from typing import Protocol

from ..dtos.InputOrder import InputOrder
from ..dtos.OutputOrder import OutputOrder


class OrderService(Protocol):
    def create_order(self, input_order: InputOrder) -> OutputOrder:
        pass

    def get_order(self, id_: str) -> OutputOrder:
        pass

    def get_order_by_user_id(self, user_id: str) -> OutputOrder:
        pass

    def update_order(self, id_: str, input_order: InputOrder) -> None:
        pass

    def delete_order(self, id_: str) -> None:
        pass
