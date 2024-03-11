import strawberry

from ....dtos.InputSalesItemImage import InputSalesItemImage


@strawberry.experimental.pydantic.input(
    model=InputSalesItemImage, all_fields=True
)
class InputSalesItemImage:
    pass
