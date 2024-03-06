class CircularBusRoute(BusRoute):
    def __init__(self, bus_stops: list[BusStop]):
        if not bus_stops:
            raise ValueError('Bus route must have at least one bus stop')

        self.__bus_stops: Final = bus_stops.copy()

    def get_next_bus_stop(self, current_bus_stop: BusStop) -> BusStop:
        return self.__bus_stops[0]