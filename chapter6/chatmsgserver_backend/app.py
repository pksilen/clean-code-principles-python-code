import asyncio
import sys
from threading import Thread
from uuid import uuid4

from fastapi import FastAPI, WebSocket

from .broker.adminclient.KafkaChatMsgBrokerAdminClient import (
    KafkaChatMsgBrokerAdminClient,
)
from .broker.consumer.KafkaChatMsgBrokerConsumer import (
    KafkaChatMsgBrokerConsumer,
)
from .connection.WebSocketConnection import WebSocketConnection
from .server.WebSocketChatMsgServer import WebSocketChatMsgServer
from .service.ChatMsgServiceImpl import ChatMsgServiceImpl

instance_uuid = str(uuid4())

# Create a Kafka topic for this particular microservice instance
try:
    KafkaChatMsgBrokerAdminClient().try_create_topic(instance_uuid)
except KafkaChatMsgBrokerAdminClient.CreateTopicError:
    # Log error
    sys.exit(1)

# Create and start a Kafka consumer to consume and send
# chat messages for recipients that are connected to
# this microservice instance

chat_msg_service = ChatMsgServiceImpl(instance_uuid)

chat_msg_broker_consumer = KafkaChatMsgBrokerConsumer(
    chat_msg_service, topic=instance_uuid
)


def consume_chat_msgs_from_broker():
    asyncio.run(chat_msg_broker_consumer.consume_chat_msgs())


chat_msg_consumer_thread = Thread(target=consume_chat_msgs_from_broker)
chat_msg_consumer_thread.start()

app = FastAPI()
chat_msg_server = WebSocketChatMsgServer(instance_uuid, chat_msg_service)


@app.websocket('/chat-messaging-service/{phone_number}')
async def handle_websocket(websocket: WebSocket, phone_number: str):
    connection = WebSocketConnection(websocket)
    await chat_msg_server.handle(connection, phone_number)


@app.on_event('shutdown')
def shutdown_event():
    chat_msg_broker_consumer.stop()
    chat_msg_consumer_thread.join()
    chat_msg_broker_consumer.close()
    chat_msg_server.close()
    chat_msg_service.close()
