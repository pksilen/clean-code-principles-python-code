from dependency_injector.wiring import Provide

from ..dtos.InputSalesItem import InputSalesItem
from ..dtos.OutputSalesItem import OutputSalesItem
from ..entities.SalesItem import SalesItem
from ..errors.EntityNotFoundError import EntityNotFoundError
from ..repositories.SalesItemRepository import SalesItemRepository
from ..service.SalesItemService import SalesItemService


class SalesItemServiceImpl(SalesItemService):
    # Sales item repository is provided by DI
    __sales_item_repository: SalesItemRepository = Provide[
        'sales_item_repository'
    ]

    def create_sales_item(
        self, input_sales_item: InputSalesItem
    ) -> OutputSalesItem:
        sales_item = SalesItem.create_from(input_sales_item)
        self.__sales_item_repository.save(sales_item)
        return OutputSalesItem.model_validate(sales_item)

    def get_sales_items(self) -> list[OutputSalesItem]:
        return [
            OutputSalesItem.model_validate(sales_item)
            for sales_item in self.__sales_item_repository.find_all()
        ]

    def get_sales_item(self, id_: str) -> OutputSalesItem:
        sales_item = self.__sales_item_repository.find(id_)

        if sales_item is None:
            raise EntityNotFoundError('Sales item', id_)

        return OutputSalesItem.model_validate(sales_item)

    def update_sales_item(
        self, id_: str, input_sales_item: InputSalesItem
    ) -> None:
        sales_item = self.__sales_item_repository.find(id_)

        if sales_item is None:
            raise EntityNotFoundError('Sales item', id_)

        sales_item = SalesItem.create_from(input_sales_item, id_)
        self.__sales_item_repository.update(sales_item)

    def delete_sales_item(self, id_: str) -> None:
        self.__sales_item_repository.delete(id_)
