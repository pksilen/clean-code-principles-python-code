from pydantic import BaseModel, Field, PositiveInt

from .InputSalesItemImage import HttpUrlString


class OutputSalesItemImage(BaseModel):
    id: str = Field(max_length=36)
    rank: PositiveInt
    url: HttpUrlString

    class Config:
        from_attributes = True
