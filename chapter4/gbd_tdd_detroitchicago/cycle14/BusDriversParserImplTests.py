import unittest

from BusDriversParserImpl import BusDriversParserImpl
from BusDriver import BusDriver


class BusDriversParserImplTests(unittest.TestCase):
    def test_parse__with_one_driver_that_has_one_bus_stop_and_one_rumor(self):
        # GIVEN
        bus_driver_spec = 'bus-stop-a;rumor1'

        # WHEN
        bus_drivers = BusDriversParserImpl().parse([bus_driver_spec])

        # THEN
        self.__assert_has_circular_bus_route_with_one_stop(bus_drivers)
        self.assertEqual(len(bus_drivers[0].get_rumors()), 1)

    def __assert_has_circular_bus_route_with_one_stop(
        self, bus_drivers: list[BusDriver]
    ):
        self.assertEqual(len(bus_drivers), 1)
        bus_stop = bus_drivers[0].get_current_bus_stop()
        next_bus_stop = bus_drivers[0].drive_to_next_bus_stop()
        self.assertEqual(bus_stop, next_bus_stop)
