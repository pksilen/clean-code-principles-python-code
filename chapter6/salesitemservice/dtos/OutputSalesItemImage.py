from pydantic import BaseModel, Field, HttpUrl, PositiveInt


class OutputSalesItemImage(BaseModel):
    id: str = Field(max_length=36)
    rank: PositiveInt
    url: HttpUrl = Field(max_length=2048)

    class Config:
        from_attributes = True
