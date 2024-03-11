from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base
from .DbSalesItemImage import DbSalesItemImage
from ....entities.SalesItem import SalesItem


class DbSalesItem(Base):
    __tablename__ = 'salesitems'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    createdAtTimestampInMs: Mapped[int] = mapped_column(BigInteger())
    name: Mapped[str] = mapped_column(String(256))
    priceInCents: Mapped[int]
    images: Mapped[list[DbSalesItemImage]] = relationship(
        cascade='all, delete-orphan', lazy='joined'
    )

    # This is a conversion method for converting
    # a domain entity into a database entity
    # Those two can have different representations
    @staticmethod
    def create_from(sales_item: SalesItem) -> 'DbSalesItem':
        return DbSalesItem(
            **{
                'id': sales_item.id,
                'createdAtTimestampInMs': sales_item.createdAtTimestampInMs,
                'name': sales_item.name,
                'priceInCents': sales_item.priceInCents,
                'images': [
                    DbSalesItemImage(
                        **{
                            'id': image.id,
                            'rank': image.rank,
                            'url': image.url,
                        }
                    )
                    for image in sales_item.images
                ],
            }
        )

    # This is a conversion method for converting
    # a database entity into a domain entity
    # Those two can have different representations
    def to_domain_entity(self) -> SalesItem:
        return SalesItem(
            **{
                'id': self.id,
                'createdAtTimestampInMs': self.createdAtTimestampInMs,
                'name': self.name,
                'priceInCents': self.priceInCents,
                'images': [
                    {
                        'id': image.id,
                        'rank': image.rank,
                        'quantity': image.url,
                    }
                    for image in self.images
                ],
            }
        )
