import strawberry

from ..dtos.InputSalesItemImage import SalesItemImage


@strawberry.experimental.pydantic.input(
    model=SalesItemImage, all_fields=True
)
class InputSalesItemImage:
    pass
