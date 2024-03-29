import os

from dependency_injector import containers, providers

from .controllers.graphql.StrawberryGraphQlSalesItemController import (
    StrawberryGraphQlSalesItemController,
)
from .controllers.rest.RestSalesItemController import RestSalesItemController
from .controllers.websocket.WebSocketSalesItemController import (
    WebSocketSalesItemController,
)
from .repositories.MongoDbSalesItemRepository import MongoDbSalesItemRepository
from .repositories.ParamSqlSalesItemRepository import (
    ParamSqlSalesItemRepository,
)
from .repositories.orm.OrmSalesItemRepository import OrmSalesItemRepository
from .service.SalesItemServiceImpl import SalesItemServiceImpl


class DiContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            '.service.SalesItemServiceImpl',
            '.controllers.rest.RestSalesItemController',
            '.controllers.graphql.AriadneGraphQlSalesItemController',
            '.controllers.graphql.StrawberryGraphQlSalesItemController',
            '.controllers.grpc.GrpcSalesItemController',
            '.controllers.websocket.WebSocketSalesItemController',
            '.repositories.orm.OrmSalesItemRepository',
            '.repositories.ParamSqlSalesItemRepository',
            '.repositories.MongoDbSalesItemRepository',
        ]
    )

    sales_item_service = providers.Singleton(SalesItemServiceImpl)

    if os.environ['DATABASE_URL'].startswith('mongodb'):
        sales_item_repository = providers.Singleton(MongoDbSalesItemRepository)
    elif os.environ['REPOSITORY_TYPE'] == 'orm':
        sales_item_repository = providers.Singleton(OrmSalesItemRepository)
    else:
        sales_item_repository = providers.Singleton(
            ParamSqlSalesItemRepository
        )

    if os.environ['CONTROLLER_TYPE'] == 'rest':
        sales_item_controller = providers.Singleton(RestSalesItemController)
    elif os.environ['CONTROLLER_TYPE'] == 'graphql':
        sales_item_controller = providers.Singleton(
            StrawberryGraphQlSalesItemController
        )

    websocket_sales_item_controller = providers.Singleton(
        WebSocketSalesItemController
    )
