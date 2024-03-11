from uuid import uuid4

from .SalesItemImage import SalesItemImage
from ..dtos.InputSalesItem import InputSalesItem


class SalesItem:
    def __init__(self, **kwargs):
        # Generating entity id on server side is good practice
        # for high security and distributed databases
        # Having all ids as string allows represents ids
        # consistently regardless of database engine and programming
        # languages used
        self.__id = kwargs.get('id') or str(uuid4())

        self.__name = kwargs['name']
        self.__price_in_cents = kwargs['priceInCents']
        self.__images = [SalesItemImage(**image) for image in kwargs['images']]

        # Perform validation of dynamic business rules here
        # If you have a lot of validations, put them in
        # separate class(es)

    # Domain entity factory method
    # You could instantiate different types of domain entities here
    @staticmethod
    def create_from(
        input_sales_item: InputSalesItem, id_: str | None
    ) -> 'SalesItem':
        return SalesItem(**{**input_sales_item.dict(), 'id': id_})

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def priceInCents(self) -> int:
        return self.__price_in_cents

    @property
    def images(self) -> list[SalesItemImage]:
        return self.__images

    # Possible additional methods for sales item related business logic
