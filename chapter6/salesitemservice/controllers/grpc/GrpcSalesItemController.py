from dependency_injector.wiring import Provide
from google.protobuf import any_pb2, json_format
from google.rpc import code_pb2, status_pb2
from grpc_status import rpc_status
from pydantic import ValidationError

from ..dtos.InputSalesItem import InputSalesItem as PydanticInputSalesItem
from ..errors.SalesItemServiceError import SalesItemServiceError
from ..grpc.proto_to_dict import proto_to_dict
from ..grpc.sales_item_service_pb2 import (
    ErrorDetails,
    GetSalesItemsArg,
    Id,
    InputSalesItem,
    Nothing,
    OutputSalesItem,
    OutputSalesItems,
    SalesItemUpdate,
)
from ..grpc.sales_item_service_pb2_grpc import SalesItemServiceServicer
from ..service.SalesItemService import SalesItemService
from ..utils import get_stack_trace


def map_http_status_code_to_grpc_status_code(error: Exception):
    # Map HTTP status code here to
    # respective gRPC status code ...
    # Mapping info is available here:
    # https://cloud.google.com/apis/design/errors#error_model
    return code_pb2.INTERNAL


def create_status_from(error: Exception) -> status_pb2.Status:
    detail = any_pb2.Any()

    if isinstance(error, SalesItemServiceError):
        grpc_status_code = map_http_status_code_to_grpc_status_code(error)
        message = error.message

        detail.Pack(
            ErrorDetails(
                code=error.code,
                description=error.description,
                # get_stack_trace returns stack trace only
                # when environment is not production
                # otherwise it returns None
                stackTrace=get_stack_trace(error.cause),
            )
        )
    elif isinstance(error, ValidationError):
        grpc_status_code = code_pb2.INVALID_ARGUMENT
        message = 'Request validation failed'
        detail.Pack(
            ErrorDetails(
                code='RequestValidationError', description=str(error)
            )
        )
    else:
        grpc_status_code = code_pb2.INTERNAL
        message = 'Unspecified internal error'
        detail.Pack(
            ErrorDetails(
                code='UnspecifiedError',
                description=str(error),
                stackTrace=get_stack_trace(error),
            )
        )

    return status_pb2.Status(
        code=grpc_status_code,
        message=message,
        details=[detail],
    )


class GrpcSalesItemController(SalesItemServiceServicer):
    __sales_item_service: SalesItemService = Provide['sales_item_service']

    def createSalesItem(
        self, input_sales_item: InputSalesItem, context
    ) -> OutputSalesItem:
        try:
            input_sales_item_dict = proto_to_dict(input_sales_item)

            input_sales_item = PydanticInputSalesItem.parse_obj(
                input_sales_item_dict
            )

            output_sales_item_dict = (
                self.__sales_item_service.create_sales_item(
                    input_sales_item
                ).dict()
            )

            output_sales_item = OutputSalesItem()

            json_format.ParseDict(
                output_sales_item_dict, output_sales_item
            )

            return output_sales_item
        except Exception as error:
            self.__abort_with(error, context)

    def getSalesItems(
        self, get_sales_items_arg: GetSalesItemsArg, context
    ) -> OutputSalesItems:
        try:
            # NOTE! Here we don't use the input message
            # 'get_sales_items_arg' because our current
            # business logic does not support it
            output_sales_items = (
                self.__sales_item_service.get_sales_items()
            )

            output_sales_items = [
                json_format.ParseDict(
                    output_sales_item.dict(), OutputSalesItem()
                )
                for output_sales_item in output_sales_items
            ]

            return OutputSalesItems(salesItems=output_sales_items)
        except Exception as error:
            self.__abort_with(error, context)

    def getSalesItem(self, id: Id, context):
        try:
            output_sales_item_dict = (
                self.__sales_item_service.get_sales_item(id.id).dict()
            )

            output_sales_item = OutputSalesItem()

            json_format.ParseDict(
                output_sales_item_dict, output_sales_item
            )

            return output_sales_item
        except Exception as error:
            self.__abort_with(error, context)

    def updateSalesItem(self, sales_item_update: SalesItemUpdate, context):
        try:
            id_ = sales_item_update.id
            sales_item_update_dict = proto_to_dict(sales_item_update)

            sales_item_update = PydanticInputSalesItem.parse_obj(
                sales_item_update_dict
            )

            self.__sales_item_service.update_sales_item(
                id_, sales_item_update
            )

            return Nothing()
        except Exception as error:
            self.__abort_with(error, context)

    def deleteSalesItem(self, id: Id, context):
        try:
            self.__sales_item_service.delete_sales_item(id.id)
            return Nothing()
        except Exception as error:
            self.__abort_with(error, context)

    @staticmethod
    def __abort_with(error: Exception, context):
        status = create_status_from(error)
        context.abort_with_status(rpc_status.to_status(status))
