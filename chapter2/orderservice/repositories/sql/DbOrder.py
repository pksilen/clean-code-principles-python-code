from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base
from .DbOrderItem import DbOrderItem
from ...entities.Order import Order


class DbOrder(Base):
    __tablename__ = 'orders'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), index=True)
    order_items: Mapped[list[DbOrderItem]] = relationship(lazy='joined')

    # This is a conversion method for converting
    # a domain entity into a database entity
    # Those two can have different representations
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

    # This is a conversion method for converting
    # a database entity into a domain entity
    # Those two can have different representations
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
