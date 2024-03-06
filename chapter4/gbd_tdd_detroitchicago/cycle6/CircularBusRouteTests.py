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

    def test_get_next_bus_stop__when_one_bus_stop(self):
        # GIVEN
        bus_stop = BusStopImpl()
        bus_route = CircularBusRoute([bus_stop])

        # WHEN
        next_bus_stop = bus_route.get_next_bus_stop(bus_stop)

        # THEN
        self.assertEqual(next_bus_stop, bus_stop)

    def test_get_next_bus_stop__when_bus_stop_does_not_belong_to_route(self):
        # GIVEN
        bus_stop_a = BusStopImpl()
        bus_route = CircularBusRoute([bus_stop_a])
        bus_stop_b = BusStopImpl()

        try:
            # WHEN
            bus_route.get_next_bus_stop(bus_stop_b)

            self.fail('ValueError should have been raised')
        except ValueError as error:
            # THEN
            self.assertEqual(
                str(error), 'Bus stop does not belong to bus route'
            )

    def test_get_next_bus_stop__when_next_bus_stop_in_list_exists(self):
        # GIVEN
        bus_stop_a = BusStopImpl()
        bus_stop_b = BusStopImpl()
        bus_route = CircularBusRoute([bus_stop_a, bus_stop_b])

        # WHEN
        next_bus_stop = bus_route.get_next_bus_stop(bus_stop_a)

        # THEN
        self.assertEqual(next_bus_stop, bus_stop_b)

    def test_get_next_bus_stop__when_no_next_bus_stop_in_list(self):
        # GIVEN
        bus_stop_a = BusStopImpl()
        bus_stop_b = BusStopImpl()
        bus_route = CircularBusRoute([bus_stop_a, bus_stop_b])

        # WHEN
        next_bus_stop = bus_route.get_next_bus_stop(bus_stop_b)

        # THEN
        self.assertEqual(next_bus_stop, bus_stop_a)