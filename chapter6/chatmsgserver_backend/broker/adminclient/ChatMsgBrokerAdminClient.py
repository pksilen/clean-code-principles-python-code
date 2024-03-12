from typing import Protocol

from ...error.ChatMsgServerError import ChatMsgServerError


class ChatMsgBrokerAdminClient(Protocol):
    class CreateTopicError(ChatMsgServerError):
        pass

    def try_create_topic(self, name: str) -> None:
        pass
