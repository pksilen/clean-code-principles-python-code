from concurrent import futures

import grpc

from .DiContainer import DiContainer
from .controllers.grpc.GrpcSalesItemController import GrpcSalesItemController
from .controllers.grpc.sales_item_service_pb2_grpc import (
    add_SalesItemServiceServicer_to_server,
)

di_container = DiContainer()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SalesItemServiceServicer_to_server(GrpcSalesItemController(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


serve()
