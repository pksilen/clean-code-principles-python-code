from typing import Any

from ariadne import format_error, unwrap_graphql_error
from ariadne.asgi import GraphQL
from pydantic import ValidationError

from .DiContainer import DiContainer
from .common.utils.utils import create_error_dict
from .controllers.graphql.AriadneGraphQlSalesItemController import (
    executable_schema,
)
from .errors.SalesItemServiceError import SalesItemServiceError

di_container = DiContainer()


def format_custom_error(graphql_error, debug: bool = False) -> dict[str, Any]:
    error = unwrap_graphql_error(graphql_error)
    endpoint = str(graphql_error.formatted['path'][0])

    if isinstance(error, SalesItemServiceError):
        error_dict = error.to_dict(endpoint)
        return {'message': error.message, 'extensions': error_dict}

    if isinstance(error, ValidationError):
        error_dict = create_error_dict(
            error,
            400,
            'RequestValidationError',
            endpoint,
        )

        return {
            'message': 'Request validation error',
            'extensions': error_dict,
        }

    if isinstance(error, Exception):
        error_dict = create_error_dict(
            error,
            500,
            'UnspecifiedInternalError',
            endpoint,
        )

        return {
            'message': 'Unspecified internal error',
            'extensions': error_dict,
        }

    else:
        return format_error(graphql_error, debug)


app = GraphQL(executable_schema, error_formatter=format_custom_error)
