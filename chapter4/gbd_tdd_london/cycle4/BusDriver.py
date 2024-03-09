from typing import Protocol

from Rumor import Rumor


class BusDriver(Protocol):
    def get_rumors(self) -> set[Rumor]:
        pass
