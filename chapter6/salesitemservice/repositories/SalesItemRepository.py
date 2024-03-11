from typing import Protocol

from ..entities.SalesItem import SalesItem


class SalesItemRepository(Protocol):
    def save(self, sales_item: SalesItem) -> None:
        pass

    def find_all(self) -> list[SalesItem]:
        pass

    def find(self, id_: str) -> SalesItem | None:
        pass

    def update(self, sales_item: SalesItem) -> None:
        pass

    def delete(self, id_: str) -> None:
        pass
