from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from InputOrder import InputOrder
from jwt_authorizer import authorizer

app = FastAPI()

# Define a custom HTTPException handler that provides
# admin logging and metrics update
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, error: StarletteHTTPException
):
    if error.status_code == 403:
        # Audit log an unauthorized request
        pass

    # Increment 'HTTP request failures' counter by one
    # using the following metric labels: error.status_code, error.detail

    return JSONResponse({'error: ': str(error.detail)}, status_code=error.status_code)

@app.get('/sales-item-service/sales-items')
async def get_sales_items():
    # No authentication/authorization required
    # Send sales items
    pass

@app.post('/messaging-service/messages')
async def create_message(request: Request):
    authorizer.authorize(request)
    # Authenticated user can create a message

@app.get('/order-service/orders/{id}')
async def get_order(id: int, request: Request):
    authorizer.authorize_for_user_own_resources_only(
        id,
        order_service.get_order_by_id_and_user_id,
        request
    )

    # Get order identified with 'id'
    # and having user id of JWT's owner

@app.post('/order-service/orders')
async def create_order(order: InputOrder, request: Request):
    authorizer.authorize_for_self(
        order.user_id,
        request
    )

    # Create an order for the user
    # User cannot create orders for other users

@app.put('/order-service/orders/{id}')
async def update_order(id: int, order: OrderUpdate, request: Request):
    authorizer.authorize_for_user_own_resources_only(
        id,
        order_service.get_order_by_id_and_user_id,
        request
    )

    # Update an order identified with 'id'
    # and user id of JWT's owner

@app.delete('/order-service/orders/{id}')
async def delete_order(id: int, request: Request):
    authorizer.authorize_if_user_has_one_of_roles(
        ['admin'], request
    )

    # Only admin user can delete an order