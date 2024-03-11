import json
import os

from ChatMsgBrokerConsumer import ChatMsgBrokerConsumer
from confluent_kafka import Consumer, KafkaException
from Connection import Connection
from phone_nbr_to_conn_map import phone_nbr_to_conn_map


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

    def consume_chat_msgs(self) -> None:
        self.__consumer.subscribe([self.__topic])

        while self.__is_running:
            try:
                messages = self.__consumer.poll(timeout=1)

                if messages is None:
                    continue

                for message in messages:
                    if message.error():
                        raise KafkaException(message.error())
                    else:
                        chat_message_json = message.value()
                        chat_message = json.loads(chat_message_json)

                        recipient_conn = phone_nbr_to_conn_map.get(
                            chat_message.get('recipientPhoneNbr')
                        )

                        if recipient_conn:
                            recipient_conn.try_send_text(chat_message_json)
            except KafkaException:
                # Handle error ...
            except Connection.Error:
                # Handle error ...

    def stop(self) -> None:
        self.__is_running = False

    def close(self):
        self.__consumer.close()
