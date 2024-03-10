from typing import Final

from BusDriver import BusDriver
from BusStop import BusStop


class BusStopImpl(BusStop):
    def __init__(self):
        self.__bus_drivers: Final = set()

    def share_rumors_with_drivers(self) -> None:
        all_rumors = {
            rumor
            for bus_driver in self.__bus_drivers
            for rumor in bus_driver.get_rumors()
        }

        for bus_driver in self.__bus_drivers:
            bus_driver.set_rumors(all_rumors)

    def add(self, bus_driver: BusDriver) -> None:
        self.__bus_drivers.add(bus_driver)

    def remove(self, bus_driver: BusDriver) -> None:
        self.__bus_drivers.remove(bus_driver)

    def get_driver_count(self) -> int:
        return len(self.__bus_drivers)
