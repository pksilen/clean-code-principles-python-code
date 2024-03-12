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
    request: Any | None = None,
) -> dict[str, Any]:
    error_message = ' '.join(
        [word.lower() for word in re.findall('[A-Z][^A-Z]*', error_code)]
    )

    return {
        'statusCode': 400,
        'statusText': status_code_to_text[status_code],
        'endpoint': f'{request.method} {request.url}' if request else None,
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
