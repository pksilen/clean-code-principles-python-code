import os
from typing import Any

from bson.errors import BSONError, InvalidId
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from ..OrderRepository import OrderRepository
from ...entities.Order import Order
from ...errors.DatabaseError import DatabaseError
from ...errors.EntityNotFoundError import EntityNotFoundError


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

            order_dict = self.__to_dict(order)
            self.__order_coll.insert_one(order_dict)
        except PyMongoError as error:
            raise DatabaseError(error)

    def find(self, id_: str) -> Order | None:
        try:
            order_dict = self.__order_coll.find_one({'_id': id_})

            return (
                None
                if order_dict is None
                else self.__to_domain_entity(order_dict)
            )
        except InvalidId:
            raise EntityNotFoundError('Order', id_)
        except (BSONError, PyMongoError) as error:
            raise DatabaseError(error)

    @staticmethod
    def __to_dict(order: Order) -> dict[str, Any]:
        return {
            '_id': order.id,
            'userId': order.userId,
            'orderItems': [
                {
                    'id': order_item.id,
                    'salesItemId': order_item.salesItemId,
                    'quantity': order_item.quantity,
                }
                for order_item in order.orderItems
            ],
        }

    @staticmethod
    def __to_domain_entity(order_dict: dict[str, Any]) -> Order:
        id_ = order_dict['_id']
        del order_dict['_id']
        return Order(**(order_dict | {'id': str(id_)}))
