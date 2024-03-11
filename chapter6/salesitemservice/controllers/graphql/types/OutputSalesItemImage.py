import strawberry

from ....dtos.InputSalesItemImage import SalesItemImage


@strawberry.experimental.pydantic.type(model=SalesItemImage, all_fields=True)
class OutputSalesItemImage:
    pass
