from typing import Any, Protocol

from ..error.ChatMsgServerError import ChatMsgServerError


class Connection(Protocol):
    class Error(ChatMsgServerError):
        pass

    async def try_connect(self) -> None:
        pass

    async def try_send_json(self, message: dict[str, Any]) -> None:
        pass

    async def try_send_text(self, message: str) -> None:
        pass

    async def try_receive_json(self) -> dict[str, str]:
        pass

    async def try_close(self) -> None:
        pass
