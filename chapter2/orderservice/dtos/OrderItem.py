from pydantic import BaseModel, PositiveInt, Field


class OrderItem(BaseModel):
    id: str = Field(max_length=36)
    salesItemId: str = Field(max_length=36)
    quantity: PositiveInt

    class Config:
        from_attributes = True
