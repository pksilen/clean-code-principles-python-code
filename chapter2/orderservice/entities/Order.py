from uuid import uuid4

from .OrderItem import OrderItem
from ..dtos.InputOrder import InputOrder


# Domain entity than can contain business logic
class Order:
    # Perform validation of dynamic business rules here
    def __init__(self, **kwargs):
        # Generating entity id on server side is good practice
        # for high security and distributed databases
        # Having all ids as string allows represents ids
        # consistently regardless of database engine and programming
        # languages used
        self.__id = str(uuid4())

        self.__user_id = kwargs['userId']
        self.__order_items = [
            OrderItem(**order_item) for order_item in kwargs['orderItems']
        ]

    # Domain entity factory method
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
