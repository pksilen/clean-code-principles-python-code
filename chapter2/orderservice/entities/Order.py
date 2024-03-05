from uuid import uuid4

from .OrderItem import OrderItem
from ..dtos.InputOrder import InputOrder


class Order:
    def __init__(self, **kwargs):
        self.__id = str(uuid4())
        self.__user_id = kwargs['userId']
        self.__order_items = [
            OrderItem(**order_item) for order_item in kwargs['orderItems']
        ]

    @staticmethod
    def create_from(input_order: InputOrder) -> 'Order':
        return Order(**input_order.dict())

    @property
    def id(self) -> str:
        return self.__id

    @property
    def userId(self) -> str:
        return self.__user_id

    @property
    def orderItems(self) -> list[OrderItem]:
        return self.__order_items

    # Implement business logic here ...
