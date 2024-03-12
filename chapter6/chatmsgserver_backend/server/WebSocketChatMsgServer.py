from typing import Final

from fastapi import WebSocketDisconnect

from .ChatMsgServer import ChatMsgServer
from ..cache.PhoneNbrToInstanceUuidCache import PhoneNbrToInstanceUuidCache
from ..cache.RedisPhoneNbrToInstanceUuidCache import (
    RedisPhoneNbrToInstanceUuidCache,
)
from ..cache.redis_client import redis_client
from ..connection.Connection import Connection
from ..connection.phone_nbr_to_conn_map import phone_nbr_to_conn_map
from ..error.ChatMsgServerError import ChatMsgServerError
from ..service.ChatMsgService import ChatMsgService


class WebSocketChatMsgServer(ChatMsgServer):
    def __init__(self, instance_uuid: str, chat_msg_service: ChatMsgService):
        self.__instance_uuid: Final = instance_uuid
        self.__chat_msg_service = chat_msg_service
        self.__conn_to_phone_nbr_map: Final[dict[Connection, str]] = {}
        self.__cache: Final = RedisPhoneNbrToInstanceUuidCache(redis_client)

    async def handle(self, connection: Connection, phone_number: str) -> None:
        try:
            await connection.try_connect()
            phone_nbr_to_conn_map[phone_number] = connection
            self.__conn_to_phone_nbr_map[connection] = phone_number
            self.__cache.try_store(phone_number, self.__instance_uuid)

            while True:
                chat_message: dict[
                    str, str
                ] = await connection.try_receive_json()

                await self.__chat_msg_service.try_send(chat_message)
        except WebSocketDisconnect:
            self.__disconnect(connection)
        except ChatMsgServerError:
            # Handle error ...
            pass

    def close(self) -> None:
        for connection in self.__conn_to_phone_nbr_map.keys():
            try:
                connection.try_close()
            except Connection.Error:
                pass

    def __disconnect(self, connection: Connection) -> None:
        phone_number = self.__conn_to_phone_nbr_map.get(connection)

        if phone_number:
            del phone_nbr_to_conn_map[phone_number]

        del self.__conn_to_phone_nbr_map[connection]

        try:
            self.__cache.try_remove(phone_number)
        except PhoneNbrToInstanceUuidCache.Error:
            # Handle error ...
            pass
