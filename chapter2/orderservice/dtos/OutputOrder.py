from typing import Annotated

from annotated_types import Len
from pydantic import Field
from pydantic.main import BaseModel

from .OrderItem import OrderItem


class OutputOrder(BaseModel):
    id: str = Field(max_length=36)
    userId: str = Field(max_length=36)
    orderItems: Annotated[list[OrderItem], Len(max_length=500)]

    class Config:
        from_attributes = True
