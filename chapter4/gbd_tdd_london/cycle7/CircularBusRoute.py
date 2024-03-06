class CircularBusRoute(BusRoute):
    def __init__(self, bus_stops: list[BusStop]):
        self.__bus_stops: Final = bus_stops.copy()

    def get_first_bus_stop(self) -> BusStop:
        return self.__bus_stops[0]