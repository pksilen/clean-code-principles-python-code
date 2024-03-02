from pydantic import BaseModel, PositiveInt

from ..entities.OrderItem import OrderItem as OrderItemEntity


class OrderItem(BaseModel):
    id: int
    salesItemId: int
    quantity: PositiveInt

    class Config:
        from_attributes=True

    class Meta:
        orm_model = OrderItemEntity
