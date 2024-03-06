class BusDriversParser(Protocol):
    def parse(self, bus_driver_specs: list[str]) -> list[BusDriver]:
        pass