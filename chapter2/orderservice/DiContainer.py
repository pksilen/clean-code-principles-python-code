import os

from dependency_injector import containers, providers

from .controllers.RestOrderController import RestOrderController
from .repositories.mongodb.MongoDbOrderRepository import MongoDbOrderRepository
from .repositories.sql.SqlOrderRepository import SqlOrderRepository
from .services.OrderServiceImpl import OrderServiceImpl


class DiContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            '.services.OrderServiceImpl',
            '.controllers.RestOrderController',
            '.controllers.FlaskRestOrderController',
            '.controllers.GraphQlOrderController',
            '.repositories.sql.SqlOrderRepository',
        ]
    )

    order_service = providers.Singleton(OrderServiceImpl)

    if os.environ['DATABASE_URL'].startswith('mysql'):
        order_repository = providers.Singleton(SqlOrderRepository)
    else:
        order_repository = providers.Singleton(MongoDbOrderRepository)

    order_controller = providers.Singleton(RestOrderController)
    # order_controller = providers.Singleton(GraphQlOrderController)
