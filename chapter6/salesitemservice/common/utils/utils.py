import os
import re
import traceback
from datetime import datetime
from typing import Any

status_code_to_text = {400: 'Bad Request', 500: 'Internal Server Error'}


def create_error_dict(
    error: Exception,
    status_code: int,
    error_code: str,
    request_or_string: Any,
) -> dict[str, Any]:
    error_message = ' '.join(
        [word.lower() for word in re.findall('[A-Z][^A-Z]*', error_code)]
    )

    if isinstance(request_or_string, str):
        endpoint = request_or_string
    else:
        endpoint = f'{request_or_string.method} {request_or_string.url}'

    return {
        'statusCode': status_code,
        'statusText': status_code_to_text[status_code],
        'endpoint': endpoint,
        'timestamp': datetime.now().isoformat(),
        'errorCode': error_code,
        'errorMessage': error_message,
        'errorDescription': str(error),
        'stackTrace': get_stack_trace(error),
    }


def get_stack_trace(error: Exception | None):
    return (
        repr(traceback.format_exception(error))
        if error and os.environ.get('ENV') != 'production'
        else None
    )
