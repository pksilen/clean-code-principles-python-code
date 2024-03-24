from typing import Any

from dependency_injector.wiring import Provide
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from ...dtos.InputSalesItem import InputSalesItem
from ...errors.ApiError import ApiError
from ...service.SalesItemService import SalesItemService


class WebSocketSalesItemController:
    __sales_item_service: SalesItemService = Provide['sales_item_service']

    def __init__(self):
        self.__procedure_to_call_procedure = {
            'createSalesItem': self.__create_sales_item,
            'getSalesItems': self.__get_sales_items,
            'getSalesItem': self.__get_sales_item,
            'updateSalesItem': self.__update_sales_item,
            'deleteSalesItem': self.__delete_sales_item,
        }

    async def handle(self, websocket: WebSocket):
        try:
            await websocket.accept()

            while True:
                rpc_dict = await websocket.receive_json()

                call_procedure = self.__procedure_to_call_procedure[
                    rpc_dict['procedure']
                ]

                argument = rpc_dict.get('argument')
                response_dict = call_procedure(argument)
                print(response_dict)
                await websocket.send_json(response_dict)
        except WebSocketDisconnect:
            await websocket.close()
        except (KeyError, ValidationError) as error:
            pass
            # Handle request validation errors ...
        except ApiError as error:
            endpoint = rpc_dict.get('procedure')
            await websocket.send_json(error.to_dict(endpoint))
        except Exception:
            pass
            # Handle unspecified internal errors ...

    def __create_sales_item(self, input_sales_item) -> dict[str, Any]:
        input_sales_item = InputSalesItem.model_validate(input_sales_item)
        return self.__sales_item_service.create_sales_item(
            input_sales_item
        ).dict()

    def __get_sales_items(self, kwargs) -> list[dict[str, Any]]:
        return [
            sales_item.dict()
            for sales_item in self.__sales_item_service.get_sales_items()
        ]

    def __get_sales_item(self, id_: str) -> dict[str, Any]:
        return self.__sales_item_service.get_sales_item(id_).dict()

    def __update_sales_item(self, input_sales_item) -> dict[str, Any]:
        id_ = input_sales_item['id']
        input_sales_item = InputSalesItem.model_validate(input_sales_item)
        self.__sales_item_service.update_sales_item(id_, input_sales_item)
        return {}

    def __delete_sales_item(self, id_: str) -> dict[str, Any]:
        self.__sales_item_service.delete_sales_item(id_)
        return {}
