import os
from typing import Any, Final

import requests
from benedict import benedict
from jwt import PyJWKClient, PyJWKClientError, decode
from jwt.exceptions import InvalidTokenError

from Authorizer import Authorizer


class __JwtAuthorizer(Authorizer):
    IAM_ERROR: Final = 'IAM error'

    def __init__(self):
        # OpenId Connect configuration endpoint in the IAM system
        self.__oidc_config_url = os.environ['OIDC_CONFIG_URL']
        self.__jwks_client = None

        # With Keycloak you can use e.g., realm_access.roles
        self.__roles_claim_path = os.environ['JWT_ROLES_CLAIM_PATH']

        # This is the URL where you can fetch the user id for a
        # specific 'sub' claim value in the access token
        # For example: http://localhost:8082/user-service/users
        self.__get_users_url = os.environ['GET_USERS_URL']

    def authorize(self, auth_header: str | None) -> None:
        self.__decode_jwt_claims(auth_header)

    # Authorize a user to create a resource for self
    # Checks that the supplied user_id is the same as the user_id
    # of the user owning the JWT
    # Note! For some IAM systems other than Keycloak,
    # you might need to use 'uid'
    # claim instead of 'sub' to get unique user id
    def authorize_for_self(
        self, user_id: str, auth_header: str | None
    ) -> None:
        user_id_in_jwt = self.get_user_id(auth_header)

        if user_id != user_id_in_jwt:
            raise self.UnauthorizedError()

    def authorize_if_user_has_one_of_roles(
        self, allowed_roles: list[str], auth_header: str | None
    ) -> None:
        claims = self.__decode_jwt_claims(auth_header)

        try:
            roles = benedict(claims)[self.__roles_claim_path]
        except KeyError as error:
            # Log error details
            raise self.IamError()

        user_is_authorized = any(
            [True for role in roles if role in allowed_roles]
        )

        if not user_is_authorized:
            raise self.UnauthorizedError()

    def __decode_jwt_claims(self, auth_header: str | None) -> dict[str, Any]:
        if not auth_header:
            raise self.UnauthenticatedError()

        try:
            if not self.__jwks_client:
                oidc_config_response = requests.get(self.__oidc_config_url)
                oidc_config_response.raise_for_status()
                oidc_config = oidc_config_response.json()
                self.__jwks_client = PyJWKClient(oidc_config['jwks_uri'])

            jwt = auth_header.split('Bearer ')[1]
            signing_key = self.__jwks_client.get_signing_key_from_jwt(jwt)
            jwt_claims = decode(jwt, signing_key.key, algorithms=['RS256'])
        except (
            requests.RequestException,
            KeyError,
            PyJWKClientError,
        ) as error:
            # Log error details
            raise self.IamError()
        except (IndexError, InvalidTokenError):
            raise self.UnauthorizedError()

        return jwt_claims

    def get_user_id(self, auth_header: str | None) -> str:
        claims = self.__decode_jwt_claims(auth_header)

        try:
            sub_claim = claims['sub']

            users_response = requests.get(
                f'{self.__get_users_url}?sub={sub_claim}&fields=id'
            )

            users_response.raise_for_status()
            # Response JSON is expected in the form [{ "id": 12345 }]
            users = users_response.json()
        except (KeyError, requests.RequestException) as error:
            # Log error details
            raise self.IamError()

        try:
            return users[0].id
        except (IndexError, AttributeError):
            raise self.UnauthorizedError()


authorizer = __JwtAuthorizer()
