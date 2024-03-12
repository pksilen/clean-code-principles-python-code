from dependency_injector.wiring import Provide
from fastapi import APIRouter, Request

from ...common.authorizer.FakeAuthorizer import FakeAuthorizer
from ...common.decorators.audit_log import audit_log
from ...common.decorators.auth_decorators import allow_for_user_roles
from ...common.decorators.increment_counter import increment_counter
from ...common.metrics.Counter import Counter
from ...dtos.InputSalesItem import InputSalesItem
from ...dtos.OutputSalesItem import OutputSalesItem
from ...service.SalesItemService import SalesItemService


class RestSalesItemController:
    # Sales item service is provided by dependency injection
    __sales_item_service: SalesItemService = Provide['sales_item_service']
    __request_attempts = Counter('request_attempts')
    __authorizer = FakeAuthorizer()

    def __init__(self):
        self.__router = APIRouter()

        self.__router.add_api_route(
            '/sales-items/',
            self.create_sales_item,
            methods=['POST'],
            status_code=201,
            response_model=OutputSalesItem,
        )

        self.__router.add_api_route(
            '/sales-items/',
            self.get_sales_items,
            methods=['GET'],
            response_model=list[OutputSalesItem],
        )

        self.__router.add_api_route(
            '/sales-items/{id_}',
            self.get_sales_item,
            methods=['GET'],
            response_model=OutputSalesItem,
        )

        self.__router.add_api_route(
            '/sales-items/{id_}',
            self.update_sales_item,
            methods=['PUT'],
            status_code=204,
            response_model=None,
        )

        self.__router.add_api_route(
            '/sales-items/{id_}',
            self.delete_sales_item,
            methods=['DELETE'],
            status_code=204,
            response_model=None,
        )

    @property
    def router(self):
        return self.__router

    def create_sales_item(
        self, input_sales_item: InputSalesItem
    ) -> OutputSalesItem:
        return self.__sales_item_service.create_sales_item(input_sales_item)

    def get_sales_items(self) -> list[OutputSalesItem]:
        return self.__sales_item_service.get_sales_items()

    def get_sales_item(self, id_: str) -> OutputSalesItem:
        return self.__sales_item_service.get_sales_item(id_)

    def update_sales_item(
        self, id_: str, input_sales_item: InputSalesItem
    ) -> None:
        self.__sales_item_service.update_sales_item(id_, input_sales_item)

    # Below controller method has decorators for audit logging, authorization
    # and metrics update. In real-life scenario, you should have decorators
    # applied to other controller methods when relevant.
    # If you want to use the below decorators, you must specify the 'request'
    # parameter for the below method because it is used by the decorators

    # When you call this API endpoint, the following kind of output can be
    # expected in the server logs:
    #
    # Authorized for roles: ['admin']
    # API endpoint: DELETE http://localhost:8000/sales-items/dafa099d-ee55-42b5-9b54-58941c94f880 accessed from: 127.0.0.1
    # Counter request_attempts incremented by 1 with labels: {'api_endpoint': 'DELETE http://localhost:8000/sales-items'}
    @allow_for_user_roles(['admin'], __authorizer)
    @audit_log
    @increment_counter(__request_attempts)
    def delete_sales_item(self, id_: str, request: Request) -> None:
        self.__sales_item_service.delete_sales_item(id_)
