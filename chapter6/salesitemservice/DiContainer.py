from dependency_injector import containers, providers

from .controllers.RestSalesItemController import RestSalesItemController
from .controllers.StrawberryGraphQlSalesItemController import (
    StrawberryGraphQlSalesItemController,
)
from .repositories.MongoDbSalesItemRepository import (
    MongoDbSalesItemRepository,
)
from .repositories.OrmSalesItemRepository import OrmSalesItemRepository
from .repositories.ParamSqlSalesItemRepository import (
    ParamSqlSalesItemRepository,
)
from .service.SalesItemServiceImpl import SalesItemServiceImpl


class DiContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            '.service.SalesItemServiceImpl',
            '.controllers.RestSalesItemController',
            '.controllers.AriadneGraphQlSalesItemController',
            '.controllers.StrawberryGraphQlSalesItemController',
            '.controllers.GrpcSalesItemController',
            '.repositories.OrmSalesItemRepository',
            '.repositories.ParamSqlSalesItemRepository',
            '.repositories.MongoDbSalesItemRepository',
        ]
    )

    sales_item_service = providers.Singleton(SalesItemServiceImpl)
    sales_item_repository = providers.Singleton(
        ParamSqlSalesItemRepository
    )
    order_controller = providers.Singleton(RestSalesItemController)
