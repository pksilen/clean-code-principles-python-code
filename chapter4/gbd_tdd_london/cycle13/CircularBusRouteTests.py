import unittest

from BusStopImpl import BusStopImpl
from CircularBusRoute import CircularBusRoute


class CircularBusRouteTests(unittest.TestCase):
    bus_stop1 = BusStopImpl()
    bus_stop2 = BusStopImpl()

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
        bus_route = CircularBusRoute([self.bus_stop1, self.bus_stop2])

        # WHEN
        first_bus_stop = bus_route.get_first_bus_stop()

        # THEN
        self.assertEqual(first_bus_stop, self.bus_stop1)

    def test_get_next_bus_stop__when_one_bus_stop(self):
        # GIVEN
        bus_route = CircularBusRoute([self.bus_stop1])

        # WHEN
        next_bus_stop = bus_route.get_next_bus_stop(self.bus_stop1)

        # THEN
        self.assertEqual(next_bus_stop, self.bus_stop1)

    def test_get_next_bus_stop__when_bus_stop_does_not_belong_to_route(self):
        # GIVEN
        bus_route = CircularBusRoute([self.bus_stop1])

        try:
            # WHEN
            bus_route.get_next_bus_stop(self.bus_stop2)

            self.fail('ValueError should have been raised')
        except ValueError as error:
            # THEN
            self.assertEqual(
                str(error), 'Bus stop does not belong to bus route'
            )

    def test_get_next_bus_stop__when_next_bus_stop_in_list_exists(self):
        # GIVEN
        bus_route = CircularBusRoute([self.bus_stop1, self.bus_stop2])

        # WHEN
        next_bus_stop = bus_route.get_next_bus_stop(self.bus_stop1)

        # THEN
        self.assertEqual(next_bus_stop, self.bus_stop2)

    def test_get_next_bus_stop__when_no_next_bus_stop_in_list(self):
        # GIVEN
        bus_route = CircularBusRoute([self.bus_stop1, self.bus_stop2])

        # WHEN
        next_bus_stop = bus_route.get_next_bus_stop(self.bus_stop2)

        # THEN
        self.assertEqual(next_bus_stop, self.bus_stop1)
