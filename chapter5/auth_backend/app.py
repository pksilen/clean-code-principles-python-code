from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Header
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

from ApiError import ApiError
from InputOrder import InputOrder
from jwt_authorizer import authorizer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Define a custom ApiError handler that provides
# admin logging and metrics update
@app.exception_handler(ApiError)
async def http_exception_handler(request: Request, error: ApiError):
    if error.status_code == 403:
        # Audit log an unauthorized request
        pass

    # Increment 'HTTP request failures' counter by one
    # using the following metric labels: error.status_code, error.detail

    return JSONResponse(error.to_dict(), status_code=error.status_code)


@app.get('/api/sales-item-api/sales-items')
def get_sales_items():
    # No authentication/authorization required
    # Send sales items
    pass


@app.post('/api/messaging-service/messages')
def create_message(
    request: Request, authorization: Annotated[str | None, Header()] = None
):
    print(authorization)
    authorizer.authorize(authorization)
    # Authenticated user can create a message
    print('Message created')


@app.get('/api/order-service/orders/{id}')
def get_order(id_: int, request: Request):
    user_id_from_jwt = authorizer.getUserId(
        request.headers.get('Authorization')
    )

    # Try to get order using 'user_id_from_jwt' as user id and 'id' as order id,
    # e.g. order_service.get_order(id_, user_id_from_jwt)
    # It is important to notice that when trying to retrieve
    # the order from database, both 'id_' and 'user_id_from_jwt'
    # are used as query filters
    # If the user is not allowed to access the resource
    # 404 Not Found is raised from the service method
    # This approach has the security benefit of not revealing
    # to an attacker whether an order with 'id_' exists or not


@app.post('/api/order-service/orders')
def create_order(input_order: InputOrder, request: Request):
    authorizer.authorize_for_self(
        input_order.userId, request.headers.get('Authorization')
    )

    # Create an order for the user.
    # User cannot create orders for other users


@app.put('/api/order-service/orders/{id}')
def update_order(id_: int, input_order: InputOrder, request: Request):
    user_id_from_jwt = authorizer.getUserId(
        request.headers.get('Authorization')
    )

    # order_service.update_order(id_, input_order, user_id_from_jwt)


@app.delete('/api/order-service/orders/{id}')
def delete_order(id: int, request: Request):
    authorizer.authorize_if_user_has_one_of_roles(
        ['admin'], request.headers.get('Authorization')
    )

    # Only admin user can delete an order
