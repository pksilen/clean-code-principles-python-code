from typing import Protocol


class ChatMsgBrokerConsumer(Protocol):
    async def consume_chat_msgs(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def close(self) -> None:
        pass
