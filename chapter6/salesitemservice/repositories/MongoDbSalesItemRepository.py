import os
import time
from typing import Any

from bson.errors import BSONError, InvalidId
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from ..dtos.InputSalesItem import InputSalesItem
from ..entities.SalesItem import SalesItem
from ..entities.SalesItemImage import SalesItemImage
from ..errors.DatabaseError import DatabaseError
from ..errors.EntityNotFoundError import EntityNotFoundError
from .SalesItemRepository import SalesItemRepository


class MongoDbSalesItemRepository(SalesItemRepository):
    def __init__(self):
        try:
            database_url = os.environ.get('DATABASE_URL')
            self.__client = MongoClient(database_url)
            database_name = database_url.split('/')[3]
            database = self.__client[database_name]
            self.__sales_items = database['salesitems']
        except Exception as error:
            # Log error
            raise (error)

    def save(self, input_sales_item: InputSalesItem) -> SalesItem:
        try:
            sales_item = input_sales_item.dict() | {
                'createdAtTimestampInMs': time.time_ns() / 1_000_000
            }

            self.__sales_items.insert_one(sales_item)
            return self.__create_sales_item_entity(sales_item)

        except PyMongoError as error:
            raise DatabaseError(error)

    def find_all(self) -> list[SalesItem]:
        try:
            sales_items = self.__sales_items.find()
            return [
                self.__create_sales_item_entity(sales_item)
                for sales_item in sales_items
            ]
        except PyMongoError as error:
            raise DatabaseError(error)

    def find(self, id_: str) -> SalesItem | None:
        try:
            sales_item = self.__sales_items.find_one(
                {'_id': ObjectId(id_)}
            )

            return (
                None
                if sales_item is None
                else self.__create_sales_item_entity(sales_item)
            )
        except InvalidId:
            raise EntityNotFoundError('Sales item', id_)
        except (BSONError, PyMongoError) as error:
            raise DatabaseError(error)

    def update(self, id_: str, sales_item_update: InputSalesItem) -> None:
        try:
            self.__sales_items.update_one(
                {'_id': ObjectId(id_)}, {'$set': sales_item_update.dict()}
            )
        except InvalidId:
            raise EntityNotFoundError('Sales item', id_)
        except (BSONError, PyMongoError) as error:
            raise DatabaseError(error)

    def delete(self, id_: str) -> None:
        try:
            self.__sales_items.delete_one({'_id': ObjectId(id_)})
        except InvalidId:
            pass
        except (BSONError, PyMongoError) as error:
            raise DatabaseError(error)

    @staticmethod
    def __create_sales_item_entity(sales_item: dict[str, Any]):
        id_ = sales_item['_id']
        del sales_item['_id']

        images = [
            SalesItemImage(**image) for image in sales_item['images']
        ]

        return SalesItem(
            **(sales_item | {'id': str(id_)} | {'images': images})
        )
