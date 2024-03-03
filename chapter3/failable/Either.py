from collections.abc import Callable
from typing import TypeVar, Generic

from Optional import Optional, PrivateConstructor

TLeft = TypeVar('TLeft')
TRight = TypeVar('TRight')
T = TypeVar('T')
U = TypeVar('U')


class Either(Generic[TLeft, TRight], metaclass=PrivateConstructor):
    def __init__(
        self,
        maybe_left_value: Optional[TLeft],
        maybe_right_value: Optional[TRight]
    ):
        self.__maybe_left_value = maybe_left_value
        self.__maybe_right_value = maybe_right_value

    @classmethod
    def with_left(cls, value: TLeft) -> 'Either[TLeft, TRight]':
        return cls._create(Optional.of(value), Optional.empty())

    @classmethod
    def with_right(cls, value: TRight) -> 'Either[TLeft, TRight]':
        return cls._create(Optional.empty(), Optional.of(value))

    def has_left_value(self) -> bool:
        return self.__maybe_left_value.is_present()

    def has_right_value(self) -> bool:
        return self.__maybe_right_value.is_present()

    def map_left(
        self,
        to_value: Callable[[TLeft], U]
    ) -> 'Either[U, TRight]':
        return Either._create(
            self.__maybe_left_value.map(to_value),
            self.__maybe_right_value
        )

    def map_right(
        self,
        to_value: Callable[[TRight], U]
    ) -> 'Either[TLeft, U]':
        return Either._create(
            self.__maybe_left_value,
            self.__maybe_right_value.map(to_value)
        )

    def map(
        self,
        left_to_value: Callable[[TLeft], U],
        right_to_value: Callable[[TRight], U]
    ) -> U:
        return self.__maybe_left_value.map(left_to_value).or_else_get(
            lambda: self.__maybe_right_value.map(right_to_value).try_get()
        )

    def apply(
        self,
        consume_left_value: Callable[[TLeft], None],
        consume_right_value: Callable[[TRight], None]
    ) -> None:
        self.__maybe_left_value.if_present(consume_left_value)
        self.__maybe_right_value.if_present(consume_right_value)

