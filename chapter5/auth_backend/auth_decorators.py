from collections.abc import Callable
from functools import wraps
from typing import Any

from Authorizer import Authorizer


class AuthDecorException(Exception):
    pass


def allow_any_user(handle_request):
    return handle_request


def allow_authorized_user(authorizer: Authorizer):
    def decorate(handle_request):
        @wraps(handle_request)
        async def wrapped_handle_request(*args, **kwargs):
            try:
                authorizer.authorize(kwargs['request'])
            except KeyError:
                raise AuthDecorException(
                    "Request handler must accept 'request' parameter"
                )
            return await handle_request(*args, **kwargs)

        return wrapped_handle_request

    return decorate


def allow_for_self(authorizer: Authorizer):
    def decorate(handle_request):
        @wraps(handle_request)
        async def wrapped_handle_request(*args, **kwargs):
            try:
                user_id = (
                    kwargs['user_id']
                    if kwargs.get('user_id')
                    else kwargs[
                        [key for key in kwargs.keys() if key.endswith('dto')][
                            0
                        ]
                    ].user_id
                )
                authorizer.authorize_for_user_own_resources_only(
                    user_id, kwargs['request']
                )
            except (AttributeError, IndexError, KeyError):
                raise AuthDecorException(
                    """
                    Request handler must accept 'request' parameter,
                    'user_id' integer parameter or DTO parameter
                    with name ending with 'dto'. DTO parameter
                    must have attribute 'user_id'
                    """
                )
            return await handle_request(*args, **kwargs)

        return wrapped_handle_request

    return decorate


def allow_for_user_own_resources_only(
    authorizer: Authorizer,
    get_entity_by_id_and_user_id: Callable[[int, int], Any],
):
    def decorate(handle_request):
        @wraps(handle_request)
        async def wrapped_handle_request(*args, **kwargs):
            try:
                authorizer.authorize_for_user_own_resources_only(
                    kwargs['id'],
                    get_entity_by_id_and_user_id,
                    kwargs['request'],
                )
            except (KeyError):
                raise AuthDecorException(
                    "Request handler must accept 'id' and 'request' parameters"
                )
            return await handle_request(*args, **kwargs)

        return wrapped_handle_request

    return decorate


def allow_for_user_roles(roles: list[str], authorizer: Authorizer):
    def decorate(handle_request):
        @wraps(handle_request)
        async def wrapped_handle_request(*args, **kwargs):
            try:
                authorizer.authorize_if_user_has_one_of_roles(
                    roles, kwargs['request']
                )
            except KeyError:
                raise AuthDecorException(
                    "Request handler must accept 'request' parameter"
                )
            return await handle_request(*args, **kwargs)

        return wrapped_handle_request

    return decorate
