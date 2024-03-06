import strawberry

from .InputOrderItem import InputOrderItem
from ....dtos.InputOrder import InputOrder


@strawberry.experimental.pydantic.input(model=InputOrder)
class InputOrder:
    userId: strawberry.auto
    orderItems: list[InputOrderItem]
