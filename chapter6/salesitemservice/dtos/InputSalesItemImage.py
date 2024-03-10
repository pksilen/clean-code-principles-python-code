from pydantic import BaseModel, HttpUrl, PositiveInt


class InputSalesItemImage(BaseModel):
    rank: PositiveInt
    url: HttpUrl = Field(max_length=2048)

