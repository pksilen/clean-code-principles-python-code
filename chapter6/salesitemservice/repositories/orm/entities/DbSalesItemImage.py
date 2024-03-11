from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class DbSalesItemImage(Base):
    __tablename__ = 'salesitemimages'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    rank: Mapped[int]
    url: Mapped[str] = mapped_column(String(2084))
    salesItemId: Mapped[int] = mapped_column(ForeignKey('salesitems.id'))
