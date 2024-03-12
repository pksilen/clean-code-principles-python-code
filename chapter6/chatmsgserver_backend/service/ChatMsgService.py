from typing import Protocol


class ChatMsgService(Protocol):
    async def try_send(self, chat_message: dict[str, str]) -> None:
        pass
