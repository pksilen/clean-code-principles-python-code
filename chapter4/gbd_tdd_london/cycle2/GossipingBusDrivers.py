class GossipingBusDrivers:
    def __init__(self, bus_drivers: list[BusDriver]):
        self.__bus_drivers = bus_drivers.copy()
        self.__all_rumors = self.__get_all_rumors()

    def drive_until_all_rumors_shared(self) -> bool:
        while True:
            bus_stops = {
                bus_driver.drive_to_next_bus_stop()
                for bus_driver in self.__bus_drivers
            }

            for bus_stop in bus_stops:
                bus_stop.share_rumors_with_drivers()

            if self.__all_rumors_are_shared():
                return True

    def __get_all_rumors(self):
        return {
            rumor
            for bus_driver in self.__bus_drivers
            for rumor in bus_driver.get_rumors()
        }

    def __all_rumors_are_shared(self) -> bool:
        return all(
            [
                bus_driver.get_rumors() == self.__all_rumors
                for bus_driver in self.__bus_drivers
            ]
        )