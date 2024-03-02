from dependency_injector.wiring import Provide

from ..dtos.InputOrder import InputOrder
from ..dtos.OutputOrder import OutputOrder
from ..repositories.OrderRepository import OrderRepository
from ..services.OrderService import OrderService
from ..services.ShoppingCartService import ShoppingCartService


class OrderServiceImpl(OrderService):
    __order_repository: OrderRepository = Provide['order_repository']
    __shopping_cart_service: ShoppingCartService = Provide[
        'shopping_cart_service'
    ]

    def create(self, order: InputOrder) -> OutputOrder:
        self.__shopping_cart_service.empty_cart(order.user_id)
        return self.__order_repository.save(order)

    # Rest of the methods...
