class BusStop(Protocol):
    def share_rumors_with_drivers(self) -> None:
        pass

    def add_bus_driver(self, bus_driver: BusDriver) -> None:
        pass