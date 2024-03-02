from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base
from .OrderItem import OrderItem


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    userId: Mapped[int] = mapped_column(BigInteger(), index=True)
    orderItems: Mapped[list[OrderItem]] = relationship(lazy='joined')
