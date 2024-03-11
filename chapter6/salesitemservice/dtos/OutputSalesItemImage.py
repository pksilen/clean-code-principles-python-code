from pydantic import BaseModel, Field, HttpUrl, PositiveInt


class OutputSalesItemImage(BaseModel):
    id: str = Field(max_length=36)
    rank: PositiveInt
    url: HttpUrl

    class Config:
        from_attributes = True
