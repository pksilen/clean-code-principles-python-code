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
        bus_stop_name, rumor_name = bus_driver_spec.split(';')

        if self.__name_to_bus_stop.get(bus_stop_name) is None:
            self.__name_to_bus_stop[bus_stop_name] = BusStopImpl()

        if self.__name_to_rumor.get(rumor_name) is None:
            self.__name_to_rumor[rumor_name] = Rumor()

        return BusDriverImpl(
            CircularBusRoute([self.__name_to_bus_stop[bus_stop_name]]),
            {self.__name_to_rumor[rumor_name]},
        )