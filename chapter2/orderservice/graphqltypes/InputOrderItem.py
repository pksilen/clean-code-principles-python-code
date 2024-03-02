import strawberry

from ..dtos.OrderItem import OrderItem


@strawberry.experimental.pydantic.input(model=OrderItem, all_fields=True)
class InputOrderItem:
    pass
