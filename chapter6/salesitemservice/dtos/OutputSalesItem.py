from pydantic import BaseModel, Field, PositiveInt

from .OutputSalesItemImage import OutputSalesItemImage


class OutputSalesItem(BaseModel):
    id: str = Field(max_length=36)
    createdAtTimestampInMs: PositiveInt
    name: str = Field(max_length=256)
    priceInCents: int
    images: list[OutputSalesItemImage] = Field(max_items=25)

    class Config:
        from_attributes = True
