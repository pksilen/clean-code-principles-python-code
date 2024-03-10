from functools import wraps


def audit_log(handle_request):
    @wraps(handle_request)
    def wrapped_handle_request(*args, **kwargs):
        method = kwargs['request'].method
        url = kwargs['request'].url
        client_host = kwargs['request'].client.host
        print(f'API endpoint: {method} {url} accessed from: {client_host}')
        return handle_request(*args, **kwargs)

    return wrapped_handle_request
