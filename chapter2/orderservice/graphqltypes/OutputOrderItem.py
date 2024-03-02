import strawberry

from ..dtos.OrderItem import OrderItem


@strawberry.experimental.pydantic.type(model=OrderItem, all_fields=True)
class OutputOrderItem:
    pass
