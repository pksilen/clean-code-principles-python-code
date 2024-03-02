from pydantic.main import BaseModel

from .OrderItem import OrderItem


class OutputOrder(BaseModel):
    id: str
    userId: str
    orderItems: list[OrderItem]

    class Config:
        orm_mode = True
