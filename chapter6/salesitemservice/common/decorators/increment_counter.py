from functools import wraps


def increment_counter(counter):
    def decorate(handle_request):
        @wraps(handle_request)
        def wrapped_handle_request(*args, **kwargs):
            method = kwargs['request'].method
            url = str(kwargs['request'].url)
            endpoint = '/'.join(url.split('/')[:4])
            counter.increment(1, {'api_endpoint': f'{method} {endpoint}'})
            return handle_request(*args, **kwargs)

        return wrapped_handle_request

    return decorate
