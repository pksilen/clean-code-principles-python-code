class BusRoute(Protocol):
    def get_next_bus_stop(self, current_bus_stop: BusStop):
        pass

    def get_first_bus_stop(self) -> BusStop:
        pass