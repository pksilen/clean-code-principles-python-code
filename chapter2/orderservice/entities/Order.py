from uuid import uuid4

from .OrderItem import OrderItem
from ..dtos.InputOrder import InputOrder


# Domain entity than can contain business logic
class Order:
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

        # Perform validation of dynamic business rules here

    # Domain entity factory method
    #
    # You could instantiate different types of domain entities here
    # Suppose we had a 'type' field in the input order.
    # Based on that field's value, we could create either
    # `BusinessOrder` or `ConsumerOrder` domain entity instance.
    # `BusinessOrder` or `ConsumerOrder` classes could derive from
    # a common `Order` domain entity class
    @staticmethod
    def create_from(input_order: InputOrder) -> 'Order':
        return Order(**input_order.dict())

    @property
    def id(self) -> str:
        return self.__id

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def order_items(self) -> list[OrderItem]:
        return self.__order_items

    # Implement business logic here ...
