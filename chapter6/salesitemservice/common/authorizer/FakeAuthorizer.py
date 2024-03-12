from .Authorizer import Authorizer


class FakeAuthorizer(Authorizer):
    def authorize_if_user_has_one_of_roles(
        self, allowed_roles: list[str], auth_header: str
    ) -> None:
        print(f'Authorized for roles: {allowed_roles}')
