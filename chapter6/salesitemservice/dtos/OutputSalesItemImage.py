from pydantic import BaseModel, Field, HttpUrl, PositiveInt


class InputSalesItemImage(BaseModel):
    id: str = Field(max_length=36)
    rank: PositiveInt
    url: HttpUrl = Field(max_length=2048)

