from typing import Protocol

from .WebSocketExampleError import WebSocketExampleError


class ChatMsgBrokerAdminClient(Protocol):
    class CreateTopicError(WebSocketExampleError):
        pass

    def try_create_topic(self, name: str) -> None:
        pass
