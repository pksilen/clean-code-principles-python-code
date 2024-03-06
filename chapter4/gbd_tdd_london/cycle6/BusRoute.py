class BusRoute(Protocol):

    def get_first_bus_stop(self) -> BusStop:
        pass