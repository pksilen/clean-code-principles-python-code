from functools import wraps

from ..authorizer.Authorizer import Authorizer


def allow_for_user_roles(roles: list[str], authorizer: Authorizer):
    def decorate(handle_request):
        @wraps(handle_request)
        def wrapped_handle_request(*args, **kwargs):
            authorizer.authorize_if_user_has_one_of_roles(
                roles, kwargs['request']
            )

            return handle_request(*args, **kwargs)

        return wrapped_handle_request

    return decorate
