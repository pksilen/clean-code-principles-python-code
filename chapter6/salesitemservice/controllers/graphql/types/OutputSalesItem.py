import strawberry

from .OutputSalesItemImage import OutputSalesItemImage
from ....dtos.OutputSalesItem import OutputSalesItem


@strawberry.experimental.pydantic.type(model=OutputSalesItem)
class OutputSalesItem:
    id: strawberry.auto
    createdAtTimestampInMs: str
    name: strawberry.auto
    priceInCents: strawberry.auto
    images: list[OutputSalesItemImage]
