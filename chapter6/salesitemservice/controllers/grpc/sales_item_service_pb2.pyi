from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetSalesItemsArg(_message.Message):
    __slots__ = ["sortByField", "sortDirection", "offset", "limit"]
    SORTBYFIELD_FIELD_NUMBER: _ClassVar[int]
    SORTDIRECTION_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    sortByField: str
    sortDirection: str
    offset: int
    limit: int
    def __init__(self, sortByField: _Optional[str] = ..., sortDirection: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class Nothing(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Image(_message.Message):
    __slots__ = ["id", "rank", "url"]
    ID_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    id: int
    rank: int
    url: str
    def __init__(self, id: _Optional[int] = ..., rank: _Optional[int] = ..., url: _Optional[str] = ...) -> None: ...

class InputSalesItem(_message.Message):
    __slots__ = ["name", "priceInCents", "images"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICEINCENTS_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    name: str
    priceInCents: int
    images: _containers.RepeatedCompositeFieldContainer[Image]
    def __init__(self, name: _Optional[str] = ..., priceInCents: _Optional[int] = ..., images: _Optional[_Iterable[_Union[Image, _Mapping]]] = ...) -> None: ...

class SalesItemUpdate(_message.Message):
    __slots__ = ["id", "name", "priceInCents", "images"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICEINCENTS_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    priceInCents: int
    images: _containers.RepeatedCompositeFieldContainer[Image]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., priceInCents: _Optional[int] = ..., images: _Optional[_Iterable[_Union[Image, _Mapping]]] = ...) -> None: ...

class OutputSalesItem(_message.Message):
    __slots__ = ["id", "createdAtTimestampInMs", "name", "priceInCents", "images"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATEDATTIMESTAMPINMS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICEINCENTS_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    id: str
    createdAtTimestampInMs: int
    name: str
    priceInCents: int
    images: _containers.RepeatedCompositeFieldContainer[Image]
    def __init__(self, id: _Optional[str] = ..., createdAtTimestampInMs: _Optional[int] = ..., name: _Optional[str] = ..., priceInCents: _Optional[int] = ..., images: _Optional[_Iterable[_Union[Image, _Mapping]]] = ...) -> None: ...

class Id(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class OutputSalesItems(_message.Message):
    __slots__ = ["salesItems"]
    SALESITEMS_FIELD_NUMBER: _ClassVar[int]
    salesItems: _containers.RepeatedCompositeFieldContainer[OutputSalesItem]
    def __init__(self, salesItems: _Optional[_Iterable[_Union[OutputSalesItem, _Mapping]]] = ...) -> None: ...

class ErrorDetails(_message.Message):
    __slots__ = ["code", "description", "stackTrace"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STACKTRACE_FIELD_NUMBER: _ClassVar[int]
    code: str
    description: str
    stackTrace: str
    def __init__(self, code: _Optional[str] = ..., description: _Optional[str] = ..., stackTrace: _Optional[str] = ...) -> None: ...
