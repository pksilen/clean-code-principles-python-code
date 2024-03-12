from typing import Protocol


class Authorizer(Protocol):
    # Rest of auth methods ...

    def authorize_if_user_has_one_of_roles(
        self, allowed_roles: list[str], auth_header: str
    ) -> None:
        pass
