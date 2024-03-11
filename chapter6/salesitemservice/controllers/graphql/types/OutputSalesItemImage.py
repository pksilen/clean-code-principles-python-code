import strawberry

from ....dtos.OutputSalesItemImage import OutputSalesItemImage


@strawberry.experimental.pydantic.type(
    model=OutputSalesItemImage, all_fields=True
)
class OutputSalesItemImage:
    pass
