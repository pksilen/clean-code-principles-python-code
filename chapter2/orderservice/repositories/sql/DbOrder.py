from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...entities.Order import Order
from .Base import Base
from .DbOrderItem import DbOrderItem


class DbOrder(Base):
    __tablename__ = 'orders'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), index=True)
    order_items: Mapped[list[DbOrderItem]] = relationship(lazy='joined')

    @staticmethod
    def create_from(order: Order) -> 'DbOrder':
        return DbOrder(
            **{
                'id': order.id,
                'user_id': order.userId,
                'order_items': [
                    DbOrderItem(
                        **{
                            'id': order_item.id,
                            'sales_item_id': order_item.salesItemId,
                            'quantity': order_item.quantity,
                        }
                    )
                    for order_item in order.orderItems
                ],
            }
        )

    def to_domain_entity(self) -> Order:
        return Order(
            **{
                'id': self.id,
                'userId': self.user_id,
                'orderItems': [
                    {
                        'id': order_item.id,
                        'salesItemId': order_item.sales_item_id,
                        'quantity': order_item.quantity,
                    }
                    for order_item in self.order_items
                ],
            }
        )
