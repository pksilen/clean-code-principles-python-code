from dependency_injector.wiring import Provide

from ..dtos.InputOrder import InputOrder
from ..dtos.OutputOrder import OutputOrder
from ..entities.Order import Order
from ..errors.EntityNotFoundError import EntityNotFoundError
from ..repositories.OrderRepository import OrderRepository
from ..services.OrderService import OrderService


class OrderServiceImpl(OrderService):
    __order_repository: OrderRepository = Provide['order_repository']

    def create_order(self, input_order: InputOrder) -> OutputOrder:
        # Input DTO is converted to valid domain entity
        order = Order.create_from(input_order)

        # If your model had additional business logic, you
        # could perform it here using domain entity and/or
        # domain service methods
        # Do not inline all the business logic code here, but
        # create separate methods either in domain entity or
        # domain service classes.
        # This example does not have any additional business
        # logic

        # Domain entity is persisted
        # Repository converts the domain entity into database entity
        self.__order_repository.save(order)

        # Domain entity is converted to output DTO
        return OutputOrder.model_validate(order)

    def get_order(self, id_: str) -> OutputOrder:
        # If found, repository returns a valid domain entity
        # by converting a found database entity into domain entity
        order = self.__order_repository.find(id_)

        if order is None:
            raise EntityNotFoundError('Order', id_)

        # Domain entity is converted to output DTO
        return OutputOrder.model_validate(order)
