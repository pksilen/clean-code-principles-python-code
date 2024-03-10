from typing import Final

from cycle9.BusRoute import BusRoute
from cycle9.BusStop import BusStop


class CircularBusRoute(BusRoute):
    def __init__(self, bus_stops: list[BusStop]):
        if not bus_stops:
            raise ValueError('Bus route must have at least one bus stop')

        self.__bus_stops: Final = bus_stops.copy()
        self.__bus_stop_count: Final = len(bus_stops)

    def get_next_bus_stop(self, current_bus_stop: BusStop) -> BusStop:
        try:
            curr_bus_stop_index = self.__bus_stops.index(current_bus_stop)
        except ValueError:
            raise ValueError('Bus stop does not belong to bus route')

        next_bus_stop_index = (curr_bus_stop_index + 1) % self.__bus_stop_count

        return self.__bus_stops[next_bus_stop_index]

    def get_first_bus_stop(self) -> BusStop:
        return self.__bus_stops[0]
