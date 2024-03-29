from BusDriver import BusDriver
from Rumor import Rumor


class BusDriverImpl(BusDriver):
    def __init__(self, rumors: set[Rumor]):
        self.__rumors = rumors.copy()

    def get_rumors(self) -> set[Rumor]:
        return self.__rumors

    def set_rumors(self, rumors: set[Rumor]) -> None:
        self.__rumors = rumors.copy()
