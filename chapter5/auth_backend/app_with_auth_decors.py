from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Header
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

from ApiError import ApiError
from InputOrder import InputOrder
from auth_decorators import (
    allow_any_user,
    allow_authorized_user,
    allow_for_self,
    allow_for_user_roles,
)
from jwt_authorizer import authorizer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Do not allow wildcard origin in production environment
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


@app.get('/api/sales-item-service/sales-items')
@allow_any_user
def get_sales_items():
    # No authentication/authorization required
    # Send sales items
    pass


@app.post('/api/messaging-service/messages')
@allow_authorized_user(authorizer)
def create_message(authorization: Annotated[str | None, Header()] = None):
    # Authenticated user can create a message
    print('Message created')


@app.get('/api/order-service/orders/{id}')
def get_order(id_: int, authorization: Annotated[str | None, Header()] = None):
    user_id_from_jwt = authorizer.getUserId(authorization)

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
@allow_for_self(authorizer)
def create_order(
    input_order: InputOrder,
    authorization: Annotated[str | None, Header()] = None,
):
    authorizer.authorize_for_self(input_order.userId, authorization)
    # Create an order for the user.
    # User cannot create orders for other users


@app.put('/api/order-service/orders/{id}')
def update_order(
    id_: int,
    input_order: InputOrder,
    authorization: Annotated[str | None, Header()] = None,
):
    user_id_from_jwt = authorizer.getUserId(authorization)
    # order_service.update_order(id_, input_order, user_id_from_jwt)


@app.delete('/api/order-service/orders/{id}')
@allow_for_user_roles(['admin'], authorizer)
def delete_order(
    id: int, authorization: Annotated[str | None, Header()] = None
):
    authorizer.authorize_if_user_has_one_of_roles(['admin'], authorization)
    # Only admin user can delete an order
