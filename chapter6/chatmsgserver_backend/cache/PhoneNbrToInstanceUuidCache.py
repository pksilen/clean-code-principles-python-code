from typing import Protocol

from ..error.ChatMsgServerError import ChatMsgServerError


class PhoneNbrToInstanceUuidCache(Protocol):
    class Error(ChatMsgServerError):
        pass

    def retrieve_instance_uuid(self, phone_number: str | None) -> str | None:
        pass

    def try_store(self, phone_number: str, instance_uuid: str) -> None:
        pass

    def try_remove(self, phone_number: str) -> None:
        pass
