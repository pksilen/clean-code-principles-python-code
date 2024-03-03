from collections.abc import Callable
from typing import Generic, TypeVar, Any

T = TypeVar('T')
U = TypeVar('U')


class PrivateConstructor(type):
    def __call__(
        cls: type[T],
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
     ):
        raise TypeError('Constructor is private')

    def _create(
        cls: type[T],
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> T:
        return super().__call__(*args, **kwargs)


class Optional(Generic[T], metaclass=PrivateConstructor):
    def __init__(self, value: T | None):
        self.__value = value

    @classmethod
    def of(cls, value: T) -> 'Optional[T]':
        return cls._create(value)

    @classmethod
    def of_nullable(cls, value: T | None) -> 'Optional[T]':
        return cls._create(value)

    @classmethod
    def empty(cls) -> 'Optional[T]':
        return cls._create(None)

    def is_empty(self) -> bool:
        return True if self.__value is None else False

    def is_present(self) -> bool:
        return False if self.__value is None else True

    def try_get(self) -> T:
        if self.__value is None:
            raise ValueError('No value to get')
        return self.__value

    def try_get_or_else_raise(self, error: Exception):
        if self.__value is None:
            raise error
        return self.__value

    def if_present(self, consume: Callable[[T], None]) -> 'Optional[T]':
        if self.__value is not None:
            consume(self.__value)
        return self

    def or_else(self, other_value: T) -> T:
        return other_value if self.__value is None else self.__value

    def or_else_get(self, supply_value: Callable[[], T]) -> T:
        return supply_value() if self.__value is None else self.__value

    def map(self, map_: Callable[[T], U | None]) -> 'Optional[U]':
        return (
            self
            if self.__value is None
            else self.of_nullable(map_(self.__value))
        )

    def flat_map(self, map_: Callable[[T], 'Optional[U]']) -> 'Optional[U]':
        return self if self.__value is None else map_(self.__value)
