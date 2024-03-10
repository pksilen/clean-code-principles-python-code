from pydantic import BaseModel, Field

from .InputSalesItemImage import InputSalesItemImage


class InputSalesItem(BaseModel):
    name: str = Field(max_length=256)
    # We accept negative prices for sales items that act
    # as discount items
    priceInCents: int
    images: list[InputSalesItemImage] = Field(max_items=25)

