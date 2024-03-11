import os
from uuid import uuid4

from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from .entities.Base import Base
from .entities.DbSalesItem import DbSalesItem
from .entities.DbSalesItemImage import DbSalesItemImage
from ..SalesItemRepository import SalesItemRepository
from ...entities.SalesItem import SalesItem
from ...errors.DatabaseError import DatabaseError


class OrmSalesItemRepository(SalesItemRepository):
    def __init__(self):
        try:
            engine = create_engine(os.environ.get('DATABASE_URL'))
            self.__SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=engine
            )
            Base.metadata.create_all(bind=engine)
        except SQLAlchemyError as error:
            # Log error
            raise error

    def save(self, sales_item: SalesItem) -> None:
        try:
            with self.__SessionLocal() as db_session:
                db_sales_item = DbSalesItem.create_from(sales_item)
                db_session.add(db_sales_item)
                db_session.commit()
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def find_all(self) -> list[SalesItem]:
        try:
            with self.__SessionLocal() as db_session:
                db_sales_items = (
                    db_session.scalars(select(DbSalesItem)).unique().all()
                )

                return [
                    db_sales_item.to_domain_entity()
                    for db_sales_item in db_sales_items
                ]
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def find(self, id_: str) -> SalesItem | None:
        try:
            with self.__SessionLocal() as db_session:
                db_sales_item = db_session.get(DbSalesItem, id_)

                return (
                    None
                    if db_sales_item is None
                    else db_sales_item.to_domain_entity()
                )
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def update(self, sales_item: SalesItem) -> None:
        try:
            with self.__SessionLocal() as db_session:
                db_sales_item = db_session.get(DbSalesItem, sales_item.id)
                db_sales_item.name = sales_item.name
                db_sales_item.priceInCents = sales_item.priceInCents

                db_sales_item.images = [
                    DbSalesItemImage(
                        id=str(uuid4()), rank=image.rank, url=image.url
                    )
                    for image in sales_item.images
                ]

                db_session.commit()
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def delete(self, id_: str) -> None:
        try:
            with self.__SessionLocal() as db_session:
                db_sales_item = db_session.get(DbSalesItem, id_)

                if db_sales_item is not None:
                    db_session.delete(db_sales_item)
                    db_session.commit()
        except SQLAlchemyError as error:
            raise DatabaseError(error)
