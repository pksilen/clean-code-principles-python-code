import os

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from .Base import Base
from .DbOrder import Order, DbOrder
from ..OrderRepository import OrderRepository
from ...errors.DatabaseError import DatabaseError


class SqlOrderRepository(OrderRepository):
    def __init__(self):
        self.__engine = create_engine(os.environ.get('DATABASE_URL'))
        self.__SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.__engine
        )

        try:
            Base.metadata.create_all(bind=self.__engine)
        except SQLAlchemyError as error:
            # Log error
            raise error

    def save(self, db_order: Order) -> None:
        with self.__SessionLocal() as db_session:
            try:
                db_order = DbOrder.create_from(db_order)
                db_session.add(db_order)
                db_session.commit()
                db_session.refresh(db_order)
            except SQLAlchemyError as error:
                raise DatabaseError(error)

    def find(self, id_: str) -> Order | None:
        with self.__SessionLocal() as db_session:
            try:
                db_order = db_session.get(DbOrder, id_)
                return db_order.to_domain_entity() if db_order else None
            except SQLAlchemyError as error:
                raise DatabaseError(error)

    # Rest of methods...
