from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, Field

from .OrderItem import OrderItem


class InputOrder(BaseModel):
    userId: str = Field(max_length=36)
    orderItems: Annotated[list[OrderItem], Len(max_length=500)]
