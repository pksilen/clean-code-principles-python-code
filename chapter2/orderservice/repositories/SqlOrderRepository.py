import os

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from ..dtos.InputOrder import InputOrder
from ..entities.Base import Base
from ..entities.Order import Order
from ..errors.DatabaseError import DatabaseError
from ..repositories.OrderRepository import OrderRepository
from ..utils import to_entity_dict


class SqlOrderRepository(OrderRepository):
    __engine = create_engine(os.environ.get('DATABASE_URL'))
    __SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=__engine
    )

    def __init__(self):
        try:
            Base.metadata.create_all(bind=self.__engine)
        except SQLAlchemyError as error:
            # Log error
            raise error

    def save(self, input_order: InputOrder) -> Order:
        with self.__SessionLocal() as db_session:
            try:
                order = Order(**to_entity_dict(input_order))
                db_session.add(order)
                db_session.commit()
                db_session.refresh(order)
                return order
            except SQLAlchemyError as error:
                raise DatabaseError(error)

    def find(self, id_: int) -> Order | None:
        with self.__SessionLocal() as db_session:
            try:
                return db_session.get(Order, id_)
            except SQLAlchemyError as error:
                raise DatabaseError(error)

    # Rest of methods...
