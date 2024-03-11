import json
from typing import Final

from ChatMsgBrokerProducer import ChatMsgBrokerProducer
from ChatMsgServer import ChatMsgServer
from Connection import Connection
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from KafkaChatMsgBrokerProducer import KafkaChatMsgBrokerProducer
from phone_nbr_to_conn_map import phone_nbr_to_conn_map
from PhoneNbrToInstanceUuidCache import PhoneNbrToInstanceUuidCache
from redis_client import redis_client
from RedisPhoneNbrToInstanceUuidCache import (
    RedisPhoneNbrToInstanceUuidCache,
)
from WebSocketConnection import WebSocketConnection


class WebSocketChatMsgServer(ChatMsgServer):
    def __init__(self, instance_uuid: str):
        self.__instance_uuid: Final = instance_uuid
        self.__conn_to_phone_nbr_map: Final[dict[Connection, str]] = {}
        self.__chat_msg_broker_producer: Final = (
            KafkaChatMsgBrokerProducer()
        )
        self.__cache: Final = RedisPhoneNbrToInstanceUuidCache(
            redis_client
        )

    async def handle(
        self, connection: Connection, phone_number: str
    ) -> None:
        try:
            await connection.try_connect()
            phone_nbr_to_conn_map[phone_number] = connection
            self.__conn_to_phone_nbr_map[connection] = phone_number
            self.__cache.try_store(phone_number, self.__instance_uuid)

            while True:
                chat_message: dict[
                    str, str
                ] = await connection.try_receive_json()

                # Validate chat_message ...
                # Store chat message permanently using another API ...
                recipient_phone_nbr = chat_message.get('recipientPhoneNbr')

                recipient_instance_uuid = (
                    self.__cache.retrieve_instance_uuid(
                        recipient_phone_nbr
                    )
                )

                await self.__try_send(
                    chat_message, recipient_instance_uuid
                )
        except WebSocketDisconnect:
            self.__disconnect(connection)
        except PhoneNbrToInstanceUuidCache.Error:
            # Handle error ...
        except Connection.Error:
            # Handle error ...
        except ChatMsgBrokerProducer.Error:
            # Handle error ...

    def close(self) -> None:
        for connection in self.__conn_to_phone_nbr_map.keys():
            try:
                connection.try_close()
            except Connection.Error:
                pass

        self.__chat_msg_broker_producer.close()

    async def __try_send(
        self,
        chat_message: dict[str, str],
        recipient_instance_uuid: str | None,
    ) -> None:
        if recipient_instance_uuid == self.__instance_uuid:
            # Recipient has active connection on
            # the same server instance as sender
            recipient_conn = phone_nbr_to_conn_map.get(
                chat_message.get('recipientPhoneNbr')
            )

            if recipient_conn:
                await recipient_conn.try_send_json(chat_message)
        elif recipient_instance_uuid:
            # Recipient has active connection on different
            # server instance compared to sender
            chat_message_json = json.dumps(chat_message)

            self.__chat_msg_broker_producer.try_produce(
                chat_message_json, topic=recipient_instance_uuid
            )

    def __disconnect(self, connection: Connection) -> None:
        phone_number = self.__conn_to_phone_nbr_map.get(connection)

        if phone_number:
            del phone_nbr_to_conn_map[phone_number]

        del self.__conn_to_phone_nbr_map[connection]

        try:
            self.__cache.try_remove(phone_number)
        except PhoneNbrToInstanceUuidCache.Error:
            # Handle error ...
