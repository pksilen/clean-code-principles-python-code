from BusDriver import BusDriver
from BusRoute import BusRoute
from Rumor import Rumor


class BusDriverImpl(BusDriver):
    def __init__(self, bus_route: BusRoute, rumors: set[Rumor]):
        self.__rumors = rumors.copy()

    def get_rumors(self) -> set[Rumor]:
        return self.__rumors

    def set_rumors(self, rumors: set[Rumor]) -> None:
        self.__rumors = rumors.copy()
