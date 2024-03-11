from grpc_status import rpc_status

import grpc

from .grpc.sales_item_service_pb2 import (
    ErrorDetails,
    GetSalesItemsArg,
    Id,
    Image,
    InputSalesItem,
    SalesItemUpdate,
)
from .grpc.sales_item_service_pb2_grpc import SalesItemServiceStub


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        sales_item_service = SalesItemServiceStub(channel)
        input_sales_item = InputSalesItem(
            name='Test',
            priceInCents=950,
            images=[
                Image(id=11, rank=1, url='http://server.com/images/1')
            ],
        )

        try:
            sales_item = sales_item_service.createSalesItem(
                input_sales_item
            )

            id_ = sales_item.id
            print(f'Sales item with id {id_} created')

            sales_items_response = sales_item_service.getSalesItems(
                GetSalesItemsArg()
            )

            print(
                f'Nbr of sales items fetched: {len(sales_items_response.salesItems)}'
            )

            sales_item_service.updateSalesItem(
                SalesItemUpdate(
                    id=id_,
                    name='Test 2',
                    priceInCents=1950,
                    images=[
                        Image(
                            id=11, rank=1, url='http://server.com/images/1'
                        )
                    ],
                )
            )
            print(f'Sales item with id {id_} updated')
            sales_item = sales_item_service.getSalesItem(Id(id=id_))
            print(f'Sales item named {sales_item.name} fetched')
            sales_item_service.deleteSalesItem(Id(id=id_))
            print(f'Sales item with id {id_} deleted')
        except grpc.RpcError as error:
            status = rpc_status.from_call(error)
            if status:
                print(f'gRPC status code: {status.code}')
                for detail in status.details:
                    error_details = ErrorDetails()
                    detail.Unpack(error_details)
                    print(f'Error code: {error_details.code}')
                    print(f'Error message: {status.message}')
                    print(
                        f'Error description: {error_details.description}'
                    )
            else:
                print(str(error))


if __name__ == '__main__':
    run()
