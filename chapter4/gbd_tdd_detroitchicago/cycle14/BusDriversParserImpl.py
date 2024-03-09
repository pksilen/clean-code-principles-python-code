from BusDriversParser import BusDriversParser
from BusDriver import BusDriver
from Rumor import Rumor
from BusDriverImpl import BusDriverImpl
from BusStopImpl import BusStopImpl
from CircularBusRoute import CircularBusRoute


class BusDriversParserImpl(BusDriversParser):
    def parse(self, bus_driver_specs: list[str]) -> list[BusDriver]:
        return [
            self.__get_bus_driver(bus_driver_spec)
            for bus_driver_spec in bus_driver_specs
        ]

    def __get_bus_driver(self, bus_driver_spec: str) -> BusDriver:
        return BusDriverImpl(CircularBusRoute([BusStopImpl()]), {Rumor()})
