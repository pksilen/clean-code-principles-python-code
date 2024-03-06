from typing import Annotated

from annotated_types import Len
from pydantic import Field
from pydantic.main import BaseModel

from .OrderItem import OrderItem


# Output DTOs declare the structure of client output
# and related validations.
# Output DTOs are created based on domain entities
# Output DTO can, for example, miss some fields that
# are present in domain entity
# Output DTOs can make your microservice more secure
# because in case of a successful injection attack,
# output DTOs limit what data can be exposed to clients
class OutputOrder(BaseModel):
    id: str = Field(max_length=36)
    userId: str = Field(max_length=36)
    orderItems: Annotated[list[OrderItem], Len(max_length=500)]

    class Config:
        from_attributes = True
