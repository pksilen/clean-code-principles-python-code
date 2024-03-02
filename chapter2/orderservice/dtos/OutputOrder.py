from pydantic.main import BaseModel

from .OrderItem import OrderItem


class OutputOrder(BaseModel):
    id: int
    userId: int
    orderItems: list[OrderItem]

    class Config:
        from_attributes=True

