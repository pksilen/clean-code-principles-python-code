from typing import Protocol

from ..connection.Connection import Connection


class ChatMsgServer(Protocol):
    async def handle(self, connection: Connection, phone_number: str) -> None:
        pass
