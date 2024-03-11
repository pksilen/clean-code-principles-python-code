import os
from typing import Any

from bson.errors import BSONError
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from .SalesItemRepository import SalesItemRepository
from ..entities.SalesItem import SalesItem
from ..errors.DatabaseError import DatabaseError


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

    def save(self, sales_item: SalesItem) -> None:
        try:
            sales_item_dict = self.__to_dict(sales_item)
            self.__sales_items.insert_one(sales_item_dict)
        except PyMongoError as error:
            raise DatabaseError(error)

    def find_all(self) -> list[SalesItem]:
        try:
            sales_item_dicts = self.__sales_items.find()

            return [
                self.__to_domain_entity(sales_item_dict)
                for sales_item_dict in sales_item_dicts
            ]

        except PyMongoError as error:
            raise DatabaseError(error)

    def find(self, id_: str) -> SalesItem | None:
        try:
            sales_item_dict = self.__sales_items.find_one({'_id': id_})

            return (
                None
                if sales_item_dict is None
                else self.__to_domain_entity(sales_item_dict)
            )
        except (BSONError, PyMongoError) as error:
            raise DatabaseError(error)

    def update(self, sales_item: SalesItem) -> None:
        try:
            self.__sales_items.update_one(
                {'_id': sales_item.id},
                {
                    '$set': {
                        'name': sales_item.name,
                        'priceInCents': sales_item.priceInCents,
                        'images': [
                            {
                                'id': image.id,
                                'rank': image.rank,
                                'url': image.url,
                            }
                            for image in sales_item.images
                        ],
                    }
                },
            )
        except (BSONError, PyMongoError) as error:
            raise DatabaseError(error)

    def delete(self, id_: str) -> None:
        try:
            self.__sales_items.delete_one({'_id': id_})
        except (BSONError, PyMongoError) as error:
            raise DatabaseError(error)

    @staticmethod
    def __to_dict(sales_item: SalesItem) -> dict[str, Any]:
        return {
            '_id': sales_item.id,
            'createdAtTimestampInMs': sales_item.createdAtTimestampInMs,
            'name': sales_item.name,
            'priceInCents': sales_item.priceInCents,
            'images': [
                {
                    'id': image.id,
                    'rank': image.rank,
                    'url': image.url,
                }
                for image in sales_item.images
            ],
        }

    @staticmethod
    def __to_domain_entity(sales_item_dict: dict[str, Any]) -> SalesItem:
        id_ = sales_item_dict['_id']
        del sales_item_dict['_id']
        return SalesItem(**(sales_item_dict | {'id': str(id_)}))
