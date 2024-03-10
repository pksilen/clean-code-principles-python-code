from typing import Protocol

from Rumor import Rumor


class BusDriver(Protocol):
    def drive_to_next_bus_stop(self) -> 'BusStop':
        pass

    def get_rumors(self) -> set[Rumor]:
        pass
