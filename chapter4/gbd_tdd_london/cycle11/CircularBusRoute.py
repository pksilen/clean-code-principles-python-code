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

    def get_next_bus_stop(self, current_bus_stop: BusStop) -> BusStop:
        if current_bus_stop not in self.__bus_stops:
            raise ValueError('Bus stop does not belong to bus route')

        if len(self.__bus_stops) == 1:
            return self.__bus_stops[0]

        curr_bus_stop_index = self.__bus_stops.index(current_bus_stop)
        return self.__bus_stops[curr_bus_stop_index + 1]
