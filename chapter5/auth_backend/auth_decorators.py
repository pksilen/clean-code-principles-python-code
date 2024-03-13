from functools import wraps

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
                authorizer.authorize(
                    kwargs['request'].headers.get('Authorization')
                )
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
                        [
                            key
                            for key in kwargs.keys()
                            if key.startswith('input')
                        ][0]
                    ].userId
                )
                authorizer.authorize_for_self(
                    user_id, kwargs['request'].headers.get('Authorization')
                )
            except (AttributeError, IndexError, KeyError):
                raise AuthDecorException(
                    """
                    Request handler must accept 'request' parameter,
                    'user_id' parameter or DTO parameter
                    with name starting with 'input'. DTO parameter
                    must have attribute 'userId'
                    """
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
                    roles, kwargs['request'].headers.get('Authorization')
                )
            except KeyError:
                raise AuthDecorException(
                    "Request handler must accept 'request' parameter"
                )
            return await handle_request(*args, **kwargs)

        return wrapped_handle_request

    return decorate
