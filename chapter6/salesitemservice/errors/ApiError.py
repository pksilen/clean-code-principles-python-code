from typing import Final


class ApiError(Exception):
    def __init__(
        self,
        status_code: int,
        status_text: str,
        message: str,
        code: str | None = None,
        description: str | None = None,
        cause: Exception | None = None,
    ):
        self.__status_code: Final = status_code
        self.__status_text: Final = status_text
        self.__timestamp: Final = datetime.now().isoformat()
        self.__message: Final = message
        self.__code: Final = code
        self.__description: Final = description
        self.__cause: Final = cause

    @property
    def status_code(self) -> int:
        return self.__status_code

    def to_dict(self, endpoint: str) -> dict[str, Any]:
        return {
            'statusCode': self.__status_code,
            'statusText': self.__status_text,
            'endpoint': endpoint,
            'timestamp': self.__timestamp,
            'errorCode': self.__code,
            'errorMessage': self.__message,
            'errorDescription': self.__description,
            # get_stack_trace returns stack trace only
            # when environment is not production
            # otherwise it returns None
            'stackTrace': get_stack_trace(self.__cause),
        }
