import os
import time

from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from ..dtos.InputSalesItem import InputSalesItem
from ..entities.Base import Base
from ..entities.SalesItem import SalesItem
from ..errors.DatabaseError import DatabaseError
from ..errors.EntityNotFoundError import EntityNotFoundError
from ..utils import to_entity_dict
from .SalesItemRepository import SalesItemRepository


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

    def save(self, input_sales_item: InputSalesItem) -> SalesItem:
        try:
            with self.__SessionLocal() as db_session:
                sales_item = SalesItem(**to_entity_dict(input_sales_item))
                sales_item.createdAtTimestampInMs = (
                    time.time_ns() / 1_000_000
                )
                db_session.add(sales_item)
                db_session.commit()
                db_session.refresh(sales_item)
                return sales_item
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def find_all(self) -> list[SalesItem]:
        try:
            with self.__SessionLocal() as db_session:
                return db_session.scalars(select(SalesItem)).unique().all()
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def find(self, id_: str) -> SalesItem | None:
        try:
            with self.__SessionLocal() as db_session:
                return db_session.get(SalesItem, id_)
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def update(self, id_: str, sales_item_update: InputSalesItem) -> None:
        try:
            with self.__SessionLocal() as db_session:
                sales_item = db_session.get(SalesItem, id_)

                if sales_item is None:
                    raise EntityNotFoundError('Sales item', id_)

                new_sales_item = SalesItem(
                    **to_entity_dict(sales_item_update)
                )

                sales_item.name = new_sales_item.name
                sales_item.priceInCents = new_sales_item.priceInCents
                sales_item.images = new_sales_item.images
                db_session.commit()
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def delete(self, id_: str) -> None:
        try:
            with self.__SessionLocal() as db_session:
                sales_item = db_session.get(SalesItem, id_)
                if sales_item is not None:
                    db_session.delete(sales_item)
                    db_session.commit()
        except SQLAlchemyError as error:
            raise DatabaseError(error)
