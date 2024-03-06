class OrderItem:
    def __init__(self, **kwargs):
        self.__id = kwargs['id']
        self.__sales_item_id = kwargs['salesItemId']
        self.__quantity = kwargs['quantity']

    @property
    def id(self) -> str:
        return self.__id

    @property
    def salesItemId(self) -> str:
        return self.__sales_item_id

    @property
    def quantity(self) -> int:
        return self.__quantity

    # Implement business logic here ...
