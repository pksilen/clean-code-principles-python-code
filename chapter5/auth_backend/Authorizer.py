from typing import Protocol

from ApiError import ApiError


class Authorizer(Protocol):
    class UnauthenticatedError(ApiError):
        def __init__(self):
            super().__init__(401, 'Unauthorized', 'Unauthenticated')

    class UnauthorizedError(ApiError):
        def __init__(self):
            super().__init__(403, 'Forbidden', 'Unauthorized')

    class IamError(ApiError):
        def __init__(self):
            super().__init__(500, 'Internal Server Error', 'IAM error')

    def authorize(self, auth_header: str | None) -> None:
        pass

    def authorize_for_self(
        self, user_id: str, auth_header: str | None
    ) -> None:
        pass

    def authorize_if_user_has_one_of_roles(
        self, allowed_roles: list[str], auth_header: str | None
    ) -> None:
        pass

    def get_user_id(self, auth_header: str | None) -> str:
        pass
