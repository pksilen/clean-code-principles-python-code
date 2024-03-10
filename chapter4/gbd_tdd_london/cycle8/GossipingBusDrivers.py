from BusDriver import BusDriver
from BusStop import BusStop


class GossipingBusDrivers:
    def __init__(self, bus_drivers: list[BusDriver]):
        self.__bus_drivers = bus_drivers.copy()
        self.__all_rumors = self.__get_all_rumors()
        self.__driven_stop_count = 0

    def drive_until_all_rumors_shared(
        self, max_driven_stop_count: int
    ) -> bool:
        while True:
            bus_stops = {
                bus_driver.drive_to_next_bus_stop()
                for bus_driver in self.__bus_drivers
            }

            self.__driven_stop_count += 1
            self.__share_rumors(bus_stops)

            if self.__all_rumors_are_shared():
                return True
            elif self.__driven_stop_count == max_driven_stop_count:
                return False

    @staticmethod
    def __share_rumors(bus_stops: set[BusStop]):
        for bus_stop in bus_stops:
            bus_stop.share_rumors_with_drivers()

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
