from pydantic import BaseModel

from .OrderItem import OrderItem


class InputOrder(BaseModel):
    userId: int
    orderItems: list[OrderItem]
