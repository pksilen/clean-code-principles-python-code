import os

from dependency_injector import containers, providers

from .controllers.RestOrderController import RestOrderController
from .controllers.graphql.GraphQlOrderController import GraphQlOrderController
from .repositories.mongodb.MongoDbOrderRepository import MongoDbOrderRepository
from .repositories.sql.SqlOrderRepository import SqlOrderRepository
from .services.OrderServiceImpl import OrderServiceImpl


class DiContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            '.services.OrderServiceImpl',
            '.controllers.RestOrderController',
            '.controllers.FlaskRestOrderController',
            '.controllers.graphql.GraphQlOrderController',
            '.repositories.sql.SqlOrderRepository',
        ]
    )

    order_service = providers.Singleton(OrderServiceImpl)

    if os.environ['DATABASE_URL'].startswith('mysql'):
        order_repository = providers.Singleton(SqlOrderRepository)
    else:
        order_repository = providers.Singleton(MongoDbOrderRepository)

    if os.environ['CONTROLLER_TYPE'].startswith('rest'):
        order_controller = providers.Singleton(RestOrderController)
    else:
        order_controller = providers.Singleton(GraphQlOrderController)
