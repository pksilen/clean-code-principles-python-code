class SalesItemImage:
    def __init__(self, **kwargs):
        self.__id = str(uuid4())
        self.__rank = kwargs['rank']
        self.__url = kwargs['url']

    @property
    def id(self) -> str:
        return self.__id

    @property
    def rank(self) -> int:
        return self.__rank

    @property
    def url(self) -> str:
        return self.__url