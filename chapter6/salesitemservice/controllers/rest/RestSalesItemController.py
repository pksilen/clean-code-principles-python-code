from dependency_injector.wiring import Provide
from fastapi import APIRouter, Request

from ..decorators.audit_log import audit_log
from ..decorators.increment_counter import increment_counter
from ..dtos.InputSalesItem import InputSalesItem
from ..dtos.OutputSalesItem import OutputSalesItem
from ..service.SalesItemService import SalesItemService


class RestSalesItemController:
    # Sales item service is provided by dependency injection
    __sales_item_service: SalesItemService = Provide['sales_item_service']

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
        return self.__sales_item_service.create_sales_item(
            input_sales_item
        )

    def get_sales_items(self) -> list[OutputSalesItem]:
        return self.__sales_item_service.get_sales_items()

    def get_sales_item(self, id_: str) -> OutputSalesItem:
        return self.__sales_item_service.get_sales_item(id_)

    def update_sales_item(
        self, id_: str, input_sales_item: InputSalesItem
    ) -> None:
        return self.__sales_item_service.update_sales_item(
            id_, input_sales_item
        )

    def delete_sales_item(self, id_: str, request: Request) -> None:
        return self.__sales_item_service.delete_sales_item(id_)
