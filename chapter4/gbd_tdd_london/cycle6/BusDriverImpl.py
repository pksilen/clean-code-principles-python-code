class BusDriverImpl(BusDriver):
    def __init__(self, bus_route: BusRoute, rumors: set[Rumor]):
        self.__bus_route = bus_route
        self.__current_bus_stop = bus_route.get_first_bus_stop()
        self.__current_bus_stop.add(self)
        self.__rumors = rumors.copy()

    def drive_to_next_bus_stop(self) -> BusStop:
       self.__current_bus_stop.remove(self)

       self.__current_bus_stop = self.__bus_route.get_next_bus_stop(
           self.__current_bus_stop
       )

       self.__current_bus_stop.add(self)
       return self.__current_bus_stop

    def get_current_bus_stop(self) -> BusStop:
        return self.__current_bus_stop