import strawberry
from dependency_injector.wiring import Provide
from strawberry.fastapi import GraphQLRouter

from .types.InputOrder import InputOrder
from .types.OutputOrder import OutputOrder
from ...services.OrderService import OrderService

order_service: OrderService = Provide['order_service']

# In the request handler functions of the below class
# remember to add authorization, necessary audit logging and
# observability (metric updates) for production.
# Examples are provided in later chapters of this book


class GraphQlOrderController:
    # Controller methods should not contain any business logic
    # Controller method should delegate to application services (use cases)
    # Controller can only contain logic related to
    # serializing/deserializing data to/from client

    @strawberry.type
    class Query:
        @strawberry.field
        def order(self, id: str) -> OutputOrder:
            output_order = order_service.get_order(id)
            return OutputOrder.from_pydantic(output_order)

    @strawberry.type
    class Mutation:
        @strawberry.mutation
        def create_order(self, input_order: InputOrder) -> OutputOrder:
            output_order = order_service.create_order(
                input_order.to_pydantic()
            )

            return OutputOrder.from_pydantic(output_order)

    __schema = strawberry.Schema(query=Query, mutation=Mutation)
    __router = GraphQLRouter(__schema, path='/graphql')

    @property
    def router(self):
        return self.__router
