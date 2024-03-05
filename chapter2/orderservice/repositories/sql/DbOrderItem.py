from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class DbOrderItem(Base):
    __tablename__ = 'orderitems'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    sales_item_id: Mapped[str] = mapped_column(String(36))
    quantity: Mapped[int]
    order_id: Mapped[str] = mapped_column(ForeignKey('orders.id'))
