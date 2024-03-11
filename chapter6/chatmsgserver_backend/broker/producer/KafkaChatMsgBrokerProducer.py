import os

from ChatMsgBrokerProducer import ChatMsgBrokerProducer
from confluent_kafka import KafkaException, Producer


class KafkaChatMsgBrokerProducer(ChatMsgBrokerProducer):
    def __init__(self):
        config = {
            'bootstrap.servers': os.environ.get('KAFKA_BROKERS'),
            'client.id': 'chat-messaging-service',
        }

        self.__producer = Producer(config)

    def try_produce(self, chat_message_json: str, topic: str):
        def handle_error(error: KafkaException):
            if error is not None:
                raise self.Error()

        try:
            self.__producer.produce(
                topic, chat_message_json, on_delivery=handle_error
            )

            self.__producer.poll()
        except KafkaException:
            raise self.Error()

    def close(self):
        try:
            self.__producer.flush()
        except KafkaException:
            pass
