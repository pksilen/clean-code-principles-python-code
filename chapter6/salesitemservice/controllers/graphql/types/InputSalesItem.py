import strawberry

from .InputSalesItemImage import InputSalesItemImage
from ....dtos.InputSalesItem import InputSalesItem


@strawberry.experimental.pydantic.input(model=InputSalesItem)
class InputSalesItem:
    name: strawberry.auto
    priceInCents: strawberry.auto
    images: list[InputSalesItemImage]
