from typing import Protocol

from ...error.ChatMsgServerError import ChatMsgServerError


class ChatMsgBrokerProducer(Protocol):
    class Error(ChatMsgServerError):
        pass

    def try_produce(self, chat_message_json: str, topic: str):
        pass

    def close(self):
        pass
