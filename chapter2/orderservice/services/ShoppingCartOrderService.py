from dependency_injector.wiring import Provide

from ..dtos.InputOrder import InputOrder
from ..dtos.OutputOrder import OutputOrder
from ..entities.Order import Order
from ..repositories.OrderRepository import OrderRepository
from ..services.OrderService import OrderService
from ..services.ShoppingCartService import ShoppingCartService


class OrderServiceImpl(OrderService):
    __order_repository: OrderRepository = Provide['order_repository']
    __shopping_cart_service: ShoppingCartService = Provide[
        'shopping_cart_service'
    ]

    def create(self, input_order: InputOrder) -> OutputOrder:
        # Input DTO is converted to valid domain entity
        order = Order.create_from(input_order)

        # This is additional business logic
        # Note that we haven't inlined the business logic code
        # here, but we have created a separate service
        self.__shopping_cart_service.empty_cart(order.user_id)

        # Domain entity is persisted
        # Repository converts the domain entity into database entity
        self.__order_repository.save(order)

        # Domain entity is converted to output DTO
        return OutputOrder.model_validate(order)
