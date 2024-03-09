import unittest

from BusStopImpl import BusStopImpl
from CircularBusRoute import CircularBusRoute


class CircularBusRouteTests(unittest.TestCase):
    def test_get_first_bus_stop(self):
        # GIVEN
        bus_stop_a = BusStopImpl()
        bus_stop_b = BusStopImpl()
        bus_route = CircularBusRoute([bus_stop_a, bus_stop_b])

        # WHEN
        first_bus_stop = bus_route.get_first_bus_stop()

        # THEN
        self.assertEqual(first_bus_stop, bus_stop_a)
