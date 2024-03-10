from typing import Final

from BusRoute import BusRoute
from BusStop import BusStop


class CircularBusRoute(BusRoute):
    def __init__(self, bus_stops: list[BusStop]):
        if not bus_stops:
            raise ValueError('Bus route must have at least one bus stop')

        self.__bus_stops: Final = bus_stops.copy()

    def get_first_bus_stop(self) -> BusStop:
        return self.__bus_stops[0]
