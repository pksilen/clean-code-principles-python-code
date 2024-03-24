from fastapi import FastAPI, Request, WebSocket
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .DiContainer import DiContainer
from .common.utils.utils import create_error_dict
from .errors.SalesItemServiceError import SalesItemServiceError

di_container = DiContainer()
app = FastAPI()


@app.exception_handler(SalesItemServiceError)
def handle_sales_item_service_error(
    request: Request, error: SalesItemServiceError
):
    # Log error.cause if status_code >= 500

    # Increment 'request_failures' counter by one
    # with labels:
    # api_endpoint=f'{request.method} {request.url}'
    # status_code=error.status_code
    # error_code=error.code

    if hasattr(request, 'method') and hasattr(request, 'url'):
        endpoint = f'{request.method} {request.url}'
    else:
        endpoint = None

    return JSONResponse(
        status_code=error.status_code,
        content=error.to_dict(endpoint),
    )


@app.exception_handler(RequestValidationError)
def handle_request_validation_error(
    request: Request, error: RequestValidationError
):
    # Audit log

    # Increment 'request_failures' counter by one
    # with labels:
    # api_endpoint=f'{request.method} {request.url}'
    # status_code=400
    # error_code='RequestValidationError'

    return JSONResponse(
        status_code=400,
        content=create_error_dict(
            error, 400, 'RequestValidationError', request
        ),
    )


@app.exception_handler(Exception)
def handle_unspecified_error(request: Request, error: Exception):

    # Increment 'request_failures' counter by one
    # with labels:
    # api_endpoint=f'{request.method} {request.url}'
    # status_code=500
    # error_code='UnspecifiedError'

    return JSONResponse(
        status_code=500,
        content=create_error_dict(
            error, 500, 'UnspecifiedInternalError', request
        ),
    )


sales_item_controller = di_container.sales_item_controller()
app.include_router(sales_item_controller.router)

websocket_sales_item_controller = (
    di_container.websocket_sales_item_controller()
)


@app.websocket('/websocket')
async def handle_websocket(websocket: WebSocket):
    await websocket_sales_item_controller.handle(websocket)
