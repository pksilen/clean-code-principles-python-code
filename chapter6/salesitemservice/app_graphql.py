import os
from typing import Any

from ariadne import format_error, unwrap_graphql_error
from ariadne.asgi import GraphQL
from pydantic import ValidationError

from .controllers.AriadneGraphQlSalesItemController import (
    executable_schema,
)
from .DiContainer import DiContainer
from .errors.SalesItemServiceError import SalesItemServiceError
from .utils import get_stack_trace

# Remove this setting of env variable for production code!
# mysql+pymysql://root:password@localhost:3306/salesitemservice
# mongodb://localhost:27017/salesitemservice
os.environ['DATABASE_URL'] = 'mongodb://localhost:27017/salesitemservice'


di_container = DiContainer()


def format_custom_error(
    graphql_error, debug: bool = False
) -> dict[str, Any]:
    error = unwrap_graphql_error(graphql_error)

    if isinstance(error, SalesItemServiceError):
        error_dict = error.to_dict()
        return {
            'message': error_dict.message,
            'extensions': error_dict
        }

    if isinstance(error, ValidationError):
        error_response = get_error_response(error, 400, 'RequestValidationError')
        return {
            'message': error_response.message,
            'extensions': error_response
        }

    if isinstance(error, Exception):
        error_response = get_error_response(error, 500, 'UnspecifiedInternalError')
        return {
            'message': 'Unspecified internal error',
            'extensions': error_response
        }

    else:
        return format_error(graphql_error, debug)


app = GraphQL(executable_schema, error_formatter=format_custom_error)
