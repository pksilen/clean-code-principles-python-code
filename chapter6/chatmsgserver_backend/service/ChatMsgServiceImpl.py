import json
from typing import Final

from .ChatMsgService import ChatMsgService
from ..broker.producer.KafkaChatMsgBrokerProducer import (
    KafkaChatMsgBrokerProducer,
)
from ..cache.RedisPhoneNbrToInstanceUuidCache import (
    RedisPhoneNbrToInstanceUuidCache,
)
from ..cache.redis_client import redis_client
from ..connection.phone_nbr_to_conn_map import phone_nbr_to_conn_map


class ChatMsgServiceImpl(ChatMsgService):
    def __init__(self, instance_uuid: str):
        self.__instance_uuid: Final = instance_uuid
        self.__chat_msg_broker_producer: Final = KafkaChatMsgBrokerProducer()
        self.__cache: Final = RedisPhoneNbrToInstanceUuidCache(redis_client)

    async def try_send(self, chat_message: dict[str, str]) -> None:
        # Validate chat_message ...
        # Store chat message permanently using another API ...

        recipient_phone_nbr = chat_message.get('recipientPhoneNbr')

        recipient_instance_uuid = self.__cache.retrieve_instance_uuid(
            recipient_phone_nbr
        )

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

    def close(self):
        self.__chat_msg_broker_producer.close()
