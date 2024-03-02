from pydantic import BaseModel

from .OrderItem import OrderItem


class InputOrder(BaseModel):
    userId: str
    orderItems: list[OrderItem]

    class Config:
        orm_mode = True
