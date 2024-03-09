from BusDriver import BusDriver
from BusDriverImpl import BusDriverImpl
from BusDriversParser import BusDriversParser
from BusStop import BusStop
from BusStopImpl import BusStopImpl
from CircularBusRoute import CircularBusRoute
from Rumor import Rumor


class BusDriversParserImpl(BusDriversParser):
    def __init__(self):
        self.__name_to_bus_stop = {}
        self.__name_to_rumor = {}

    def parse(self, bus_driver_specs: list[str]) -> list[BusDriver]:
        return [
            self.__get_bus_driver(bus_driver_spec)
            for bus_driver_spec in bus_driver_specs
        ]

    def __get_bus_driver(self, bus_driver_spec: str) -> BusDriver:
        bus_route_spec, rumors_spec = bus_driver_spec.split(';')
        bus_stop_names = bus_route_spec.split(',')
        bus_stops = self.__get_bus_stops(bus_stop_names)
        rumor_names = rumors_spec.split(',')
        rumors = self.__get_rumors(rumor_names)
        return BusDriverImpl(CircularBusRoute(bus_stops), rumors)

    def __get_bus_stops(self, bus_stop_names: list[str]) -> list[BusStop]:
        for name in bus_stop_names:
            if self.__name_to_bus_stop.get(name) is None:
                self.__name_to_bus_stop[name] = BusStopImpl()

        return [self.__name_to_bus_stop[name] for name in bus_stop_names]

    def __get_rumors(self, rumor_names: list[str]) -> set[Rumor]:
        for name in rumor_names:
            if self.__name_to_rumor.get(name) is None:
                self.__name_to_rumor[name] = Rumor()

        return {self.__name_to_rumor[name] for name in rumor_names}
