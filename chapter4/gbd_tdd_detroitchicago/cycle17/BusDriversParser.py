from typing import Protocol

from BusDriver import BusDriver


class BusDriversParser(Protocol):
    def parse(self, bus_driver_specs: list[str]) -> list[BusDriver]:
        pass
