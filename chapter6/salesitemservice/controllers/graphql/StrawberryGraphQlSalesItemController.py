import strawberry
from dependency_injector.wiring import Provide
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from ..graphqltypes.IdReponse import IdResponse
from ..graphqltypes.InputSalesItem import InputSalesItem
from ..graphqltypes.OutputSalesItem import OutputSalesItem
from ..service.SalesItemService import SalesItemService

sales_item_service: SalesItemService = Provide['sales_item_service']


class StrawberryGraphQlSalesItemController:
    @strawberry.type
    class Query:
        @strawberry.field
        def salesItems(self, info: Info) -> list[OutputSalesItem]:
            output_sales_items = sales_item_service.get_sales_items()

            return [
                OutputSalesItem.from_pydantic(output_sales_item)
                for output_sales_item in output_sales_items
            ]

        @strawberry.field
        def salesItem(self, info: Info, id: str) -> OutputSalesItem:
            output_sales_item = sales_item_service.get_sales_item(id)
            return OutputSalesItem.from_pydantic(output_sales_item)

    @strawberry.type
    class Mutation:
        @strawberry.mutation
        def createSalesItem(
            self, info: Info, inputSalesItem: InputSalesItem
        ) -> OutputSalesItem:
            output_sales_item = sales_item_service.create_sales_item(
                inputSalesItem.to_pydantic()
            )

            return OutputSalesItem.from_pydantic(output_sales_item)

        @strawberry.mutation
        def updateSalesItem(
            self, info: Info, id: str, inputSalesItem: InputSalesItem
        ) -> IdResponse:
            sales_item_service.update_sales_item(
                id, inputSalesItem.to_pydantic()
            )

            return IdResponse(id=id)

        @strawberry.mutation
        def deleteSalesItem(self, info: Info, id: str) -> IdResponse:
            sales_item_service.delete_sales_item(id)
            return IdResponse(id=id)

    __schema = strawberry.Schema(query=Query, mutation=Mutation)
    __router = GraphQLRouter(__schema, path='/graphql')

    @property
    def router(self):
        return self.__router
