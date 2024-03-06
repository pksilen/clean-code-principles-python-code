class BusDriverImpl(BusDriver):
    def __init__(self, rumors: set[Rumor]):
        self.__rumors = rumors.copy()

    def get_rumors(self) -> set[Rumor]:
        return self.__rumors