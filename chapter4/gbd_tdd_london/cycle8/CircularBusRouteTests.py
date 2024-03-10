import unittest

from BusStopImpl import BusStopImpl
from CircularBusRoute import CircularBusRoute


class CircularBusRouteTests(unittest.TestCase):
    def test_constructor__when_no_bus_stops(self):
        try:
            # WHEN
            CircularBusRoute([])

            self.fail('ValueError should have been raised')
        except ValueError as error:
            # THEN
            self.assertEqual(
                str(error), 'Bus route must have at least one bus stop'
            )

    def test_get_first_bus_stop(self):
        # GIVEN
        bus_stop1 = BusStopImpl()
        bus_stop2 = BusStopImpl()
        bus_route = CircularBusRoute([bus_stop1, bus_stop2])

        # WHEN
        first_bus_stop = bus_route.get_first_bus_stop()

        # THEN
        self.assertEqual(first_bus_stop, bus_stop1)
