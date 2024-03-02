import strawberry

from ..dtos.InputOrder import InputOrder
from .InputOrderItem import InputOrderItem


@strawberry.experimental.pydantic.input(model=InputOrder)
class InputOrder:
    userId: strawberry.auto
    orderItems: list[InputOrderItem]
