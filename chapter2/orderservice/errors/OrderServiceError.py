from typing import Final


class OrderServiceError(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        cause: Exception | None = None,
    ):
        self.__status_code: Final = status_code
        self.__message: Final = message
        self.__cause: Final = cause

    @property
    def status_code(self) -> int:
        return self.__status_code

    @property
    def message(self) -> str:
        return self.__message

    @property
    def cause(self) -> Exception | None:
        return self.__cause
