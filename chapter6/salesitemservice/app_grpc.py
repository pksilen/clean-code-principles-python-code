import os
from concurrent import futures

import grpc

from .controllers.GrpcSalesItemController import GrpcSalesItemController
from .DiContainer import DiContainer
from .grpc.sales_item_service_pb2_grpc import (
    add_SalesItemServiceServicer_to_server,
)

di_container = DiContainer()

# Remove this setting of env variable for production code!
# mysql+pymysql://root:password@localhost:3306/salesitemservice
# mongodb://localhost:27017/salesitemservice
os.environ[
    'DATABASE_URL'
] = 'mysql+pymysql://root:password@localhost:3306/salesitemservice'


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SalesItemServiceServicer_to_server(
        GrpcSalesItemController(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


serve()
