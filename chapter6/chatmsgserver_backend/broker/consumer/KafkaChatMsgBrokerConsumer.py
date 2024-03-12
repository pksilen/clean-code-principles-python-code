import json
import os

from confluent_kafka import Consumer, KafkaException

from .ChatMsgBrokerConsumer import ChatMsgBrokerConsumer
from ...connection.Connection import Connection
from ...connection.phone_nbr_to_conn_map import phone_nbr_to_conn_map


class KafkaChatMsgBrokerConsumer(ChatMsgBrokerConsumer):
    def __init__(self, topic: str):
        self.__topic = topic

        config = {
            'bootstrap.servers': os.environ.get('KAFKA_BROKERS'),
            'group.id': 'chat-messaging-service',
            'auto.offset.reset': 'smallest',
            'enable.partition.eof': False,
        }

        self.__consumer = Consumer(config)
        self.__is_running = True

    async def consume_chat_msgs(self) -> None:
        self.__consumer.subscribe([self.__topic])

        while self.__is_running:
            try:
                message = self.__consumer.poll(timeout=1)

                if message is None:
                    continue
                elif message.error():
                    raise KafkaException(message.error())
                else:
                    chat_message_json = message.value().decode('utf-8')
                    chat_message = json.loads(chat_message_json)

                    recipient_conn = phone_nbr_to_conn_map.get(
                        chat_message.get('recipientPhoneNbr')
                    )

                    if recipient_conn:
                        await recipient_conn.try_send_text(chat_message_json)
            except KafkaException:
                # Handle error ...
                pass
            except Connection.Error:
                # Handle error ...
                pass

    def stop(self) -> None:
        self.__is_running = False

    def close(self):
        self.__consumer.close()
