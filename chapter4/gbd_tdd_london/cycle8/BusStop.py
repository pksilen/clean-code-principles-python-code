from typing import Protocol

from BusDriver import BusDriver


class BusStop(Protocol):
    def share_rumors_with_drivers(self):
        pass

    def add(self, bus_driver: BusDriver) -> None:
        pass

    def remove(self, bus_driver: BusDriver) -> None:
        pass
