import os
from typing import Any

from mysql.connector import connect
from mysql.connector.errors import Error

from .SalesItemRepository import SalesItemRepository
from ..entities.SalesItem import SalesItem
from ..entities.SalesItemImage import SalesItemImage
from ..errors.DatabaseError import DatabaseError


class ParamSqlSalesItemRepository(SalesItemRepository):
    def __init__(self):
        try:
            self.__conn_config = self.__try_create_conn_config()
            self.__try_create_db_tables_if_needed()
        except Exception as error:
            # Log error
            raise (error)

    def save(self, sales_item: SalesItem) -> None:
        connection = None

        try:
            connection = connect(**self.__conn_config)
            cursor = connection.cursor(prepared=True)

            sql_statement = (
                'INSERT INTO salesitems'
                ' (id, createdAtTimestampInMs, name, priceInCents)'
                ' VALUES (%s, %s, %s, %s)'
            )

            cursor.execute(
                sql_statement,
                (
                    sales_item.id,
                    sales_item.createdAtTimestampInMs,
                    sales_item.name,
                    sales_item.priceInCents,
                ),
            )

            self.__insert_sales_item_images(
                sales_item.id, sales_item.images, cursor
            )

            connection.commit()
        except Error as error:
            raise DatabaseError(error)
        finally:
            if connection:
                connection.close()

    def find_all(self) -> list[SalesItem]:
        connection = None

        try:
            connection = connect(**self.__conn_config)
            cursor = connection.cursor()

            sql_statement = (
                'SELECT s.id, s.createdAtTimestampInMs, s.name, s.priceInCents,'
                'si.id, si.rank, si.url '
                'FROM salesitems s '
                'LEFT JOIN salesitemimages si ON si.salesItemId = s.id'
            )

            cursor.execute(sql_statement)
            return self.__get_sales_items(cursor)
        except Error as error:
            print(error)
            raise DatabaseError(error)
        finally:
            if connection:
                connection.close()

    def find(self, id_: str) -> SalesItem | None:
        connection = None

        try:
            connection = connect(**self.__conn_config)
            cursor = connection.cursor(prepared=True)

            sql_statement = (
                'SELECT s.id, s.createdAtTimestampInMs, s.name, s.priceInCents,'
                'si.id, si.rank, si.url '
                'FROM salesitems s '
                'LEFT JOIN salesitemimages si ON si.salesItemId = s.id '
                'WHERE s.id = %s'
            )

            cursor.execute(sql_statement, (id_,))
            sales_items = self.__get_sales_items(cursor)
            return sales_items[0] if sales_items else None
        except Error as error:
            raise DatabaseError(error)
        finally:
            if connection:
                connection.close()

    def update(self, sales_item: SalesItem) -> None:
        connection = None

        try:
            connection = connect(**self.__conn_config)
            cursor = connection.cursor(prepared=True)

            sql_statement = (
                'UPDATE salesitems SET name = %s, priceInCents = %s '
                'WHERE id = %s'
            )

            cursor.execute(
                sql_statement,
                (
                    sales_item.name,
                    sales_item.priceInCents,
                    sales_item.id,
                ),
            )

            sql_statement = (
                'DELETE FROM salesitemimages WHERE salesItemId = %s'
            )

            cursor.execute(sql_statement, (sales_item.id,))

            self.__insert_sales_item_images(
                sales_item.id, sales_item.images, cursor
            )

            connection.commit()
        except Error as error:
            raise DatabaseError(error)
        finally:
            if connection:
                connection.close()

    def delete(self, id_: str) -> None:
        connection = None

        try:
            connection = connect(**self.__conn_config)
            cursor = connection.cursor()

            sql_statement = (
                'DELETE FROM salesitemimages WHERE salesItemId = %s'
            )

            cursor.execute(sql_statement, (id_,))
            sql_statement = 'DELETE FROM salesitems WHERE id = %s'
            cursor.execute(sql_statement, (id_,))
            connection.commit()
        except Error as error:
            raise DatabaseError(error)
        finally:
            if connection.is_connected():
                connection.close()

    @staticmethod
    def __try_create_conn_config() -> dict[str, Any]:
        database_url = os.environ.get('DATABASE_URL')

        user_and_password = (
            database_url.split('@')[0].split('//')[1].split(':')
        )

        host_and_port = database_url.split('@')[1].split('/')[0].split(':')
        database = database_url.split('/')[3]

        return {
            'user': user_and_password[0],
            'password': user_and_password[1],
            'host': host_and_port[0],
            'port': host_and_port[1],
            'database': database,
            'pool_name': 'salesitems',
            'pool_size': 25,
        }

    def __try_create_db_tables_if_needed(self) -> None:
        connection = connect(**self.__conn_config)
        cursor = connection.cursor()

        sql_statement = (
            'CREATE TABLE IF NOT EXISTS salesitems ('
            'id VARCHAR(36) NOT NULL,'
            'createdAtTimestampInMs BIGINT NOT NULL,'
            'name VARCHAR(256) NOT NULL,'
            'priceInCents INTEGER NOT NULL,'
            'PRIMARY KEY (id)'
            ')'
        )

        cursor.execute(sql_statement)

        sql_statement = (
            'CREATE TABLE IF NOT EXISTS salesitemimages ('
            'id VARCHAR(36) NOT NULL,'
            '`rank` INTEGER NOT NULL,'
            'url VARCHAR(2084) NOT NULL,'
            'salesItemId VARCHAR(36) NOT NULL,'
            'PRIMARY KEY (id),'
            'FOREIGN KEY (salesItemId) REFERENCES salesitems(id)'
            ')'
        )

        cursor.execute(sql_statement)
        connection.commit()
        connection.close()

    def __insert_sales_item_images(self, sales_item_id: str, images, cursor):
        for image in images:
            sql_statement = (
                'INSERT INTO salesitemimages'
                ' (id, `rank`, url, salesItemId)'
                ' VALUES (%s, %s, %s, %s)'
            )

            cursor.execute(
                sql_statement,
                (image.id, image.rank, image.url, sales_item_id),
            )

    def __get_sales_items(self, cursor) -> list[SalesItem]:
        id_to_sales_item = dict()

        for (
            id_,
            created_at_timestamp_in_ms,
            name,
            price_in_cents,
            image_id,
            image_rank,
            image_url,
        ) in cursor:
            if id_to_sales_item.get(id_) is None:
                id_to_sales_item[id_] = SalesItem(
                    id=id_,
                    createdAtTimestampInMs=created_at_timestamp_in_ms,
                    name=name,
                    priceInCents=price_in_cents,
                    images=[],
                )

            if image_id is not None:
                id_to_sales_item[id_].images.append(
                    SalesItemImage(id=image_id, rank=image_rank, url=image_url)
                )

        return list(id_to_sales_item.values())
