import os
from typing import Any

from bson.errors import BSONError, InvalidId
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from ...errors.EntityNotFoundError import EntityNotFoundError
from ...errors.DatabaseError import DatabaseError
from ..OrderRepository import OrderRepository
from ...entities.Order import Order


class MongoDbOrderRepository(OrderRepository):
    def __init__(self):
        try:
            database_url = os.environ.get('DATABASE_URL')
            self.__client = MongoClient(database_url)
            database_name = database_url.split('/')[3]
            database = self.__client[database_name]
            self.__order_coll = database['orders']
        except Exception as error:
            # Log error
            raise (error)

    def save(self, order: Order) -> None:
        try:
            order_dict = order.__dict__
            order_dict['_id'] = order.id
            del order_dict['id']
            self.__order_coll.insert_one(order_dict)
        except PyMongoError as error:
            raise DatabaseError(error)

    def find(self, id_: str) -> Order | None:
        try:
            sales_item = self.__order_coll.find_one({'_id': id_})

            return (
                None
                if sales_item is None
                else self.__create_sales_item_entity(sales_item)
            )
        except InvalidId:
            raise EntityNotFoundError('Sales item', id_)
        except (BSONError, PyMongoError) as error:
            raise DatabaseError(error)

    @staticmethod
    def __create_sales_item_entity(order_dict: dict[str, Any]):
        id_ = order_dict['_id']
        del order_dict['_id']
        return Order(**(order_dict | {'id': str(id_)}))
