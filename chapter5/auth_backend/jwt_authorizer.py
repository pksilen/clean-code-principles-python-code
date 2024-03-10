import os
from typing import Any, Final
from collections.abc import Callable

import requests
from Authorizer import Authorizer
from benedict import benedict
from fastapi import HTTPException, Request
from jwt import PyJWKClient, PyJWKClientError, decode
from jwt.exceptions import InvalidTokenError


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

    def authorize(self, request: Request) -> None:
        self.__decode_jwt_claims(request.headers.get('Authorization'))

    # Authorize a user to create a resource for self
    # Checks that the supplied user_id is the same as the user_id
    # of the user owning the JWT
    # Note! For some IAM systems other than Keycloak,
    # you might need to use 'uid'
    # claim instead of 'sub' to get unique user id
    def authorize_for_self(
        self, user_id: int, request: Request
    ) -> None:
        jwt_user_id = self.__get_jwt_user_id(request)
        user_is_authorized = user_id == jwt_user_id
        if not user_is_authorized:
            raise HTTPException(status_code=403, detail='Unauthorized')

    # Authorize a user for his/hers own resources only
    # If an entity with given id and user_id combination
    # is not found, auth error is raised
    def authorize_for_user_own_resources_only(
        self,
        id: int,
        get_entity_by_id_and_user_id: Callable[[int, int], Any],
        request: Request
    ) -> None:
        jwt_user_id = self.__get_jwt_user_id(request)

        try:
            get_entity_by_id_and_user_id(id, jwt_user_id)
        except HTTPException as error:
            if error.status_code == 404:
                raise HTTPException(status_code=403, detail='Unauthorized')
            # Log error details
            raise HTTPException(status_code=500, detail=self.IAM_ERROR)

    def authorize_if_user_has_one_of_roles(
        self, allowed_roles: list[str], request: Request
    ) -> None:
        claims = self.__decode_jwt_claims(
            request.headers.get('Authorization')
        )

        try:
            roles = benedict(claims)[self.__roles_claim_path]
        except KeyError as error:
            # Log error details
            raise HTTPException(status_code=500, detail=self.IAM_ERROR)

        user_is_authorized = any(
            [True for role in roles if role in allowed_roles]
        )
        if not user_is_authorized:
            raise HTTPException(status_code=403, detail='Unauthorized')

    def __decode_jwt_claims(
        self, auth_header: str | None
    ) -> dict[str, Any]:
        if not auth_header:
             raise HTTPException(status_code=401, detail='Unauthenticated')

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
            PyJWKClientError
        ) as error:
            # Log error details
            raise HTTPException(status_code=500, detail=self.IAM_ERROR)
        except (IndexError, InvalidTokenError):
            raise HTTPException(status_code=403, detail='Unauthorized')

        return jwt_claims

    def __get_jwt_user_id(self, request: Request) -> int:
        claims = self.__decode_jwt_claims(
            request.headers.get('Authorization')
        )

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
            raise HTTPException(status_code=500, detail=self.IAM_ERROR)

        try:
            return users[0].id
        except (IndexError, AttributeError):
            raise HTTPException(status_code=403, detail='Unauthorized')


authorizer = __JwtAuthorizer()