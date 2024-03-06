import strawberry

from .OutputOrderItem import OutputOrderItem
from ....dtos.OutputOrder import OutputOrder


@strawberry.experimental.pydantic.type(model=OutputOrder)
class OutputOrder:
    id: strawberry.auto
    userId: strawberry.auto
    orderItems: list[OutputOrderItem]
