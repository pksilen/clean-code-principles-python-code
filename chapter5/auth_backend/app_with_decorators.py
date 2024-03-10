from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from InputOrder import InputOrder
from jwt_authorizer import authorizer
from order_service import order_service
# OrderUpdate is a DTO that should not have user_id attribute,
# because it cannot be changed
from OrderUpdate import OrderUpdate

app = FastAPI()

# Define a custom HTTPException handler that provides
# admin logging and metrics update
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, error: StarletteHTTPException
):
    if error.status_code == 403:
        # Audit log an unauthorized request

    # Increment 'HTTP request failures' counter by one
    # using the following metric labels: error.status_code, error.detail

    return JSONResponse({'error: ': str(error.detail)}, status_code=error.status_code)

@app.get('/sales-item-service/sales-items')
@allow_any_user
async def get_sales_items():
    # ...

@app.post('/messaging-service/messages')
@allow_authorized_user(authorizer)
async def create_message(request: Request):
    # ...

@app.get('/order-service/orders/{id}')
@allow_for_user_own_resources_only(
    authorizer,
    order_service.get_order_by_id_and_user_id
)
async def get_order(id: int, request: Request):
    # ...

@app.post('/order-service/orders')
@allow_for_user_own_resources_only(authorizer)
async def create_order(
    order_dto: InputOrder, request: Request
):
    # ...

@app.put('/order-service/orders/{id}')
@allow_for_user_own_resources_only(
    authorizer,
    order_service.get_order_by_id_and_user_id
)
async def update_order(
    id: int, order: OrderUpdate, request: Request
):
    # ...

@app.delete('/order-service/orders/{id}')
@allow_for_user_roles(['admin'], authorizer)
async def delete_order(id: int, request: Request):
    # ...