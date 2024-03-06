class BusDriversParserImplTests(unittest.TestCase):
    def test_parse__with_one_driver_that_has_one_bus_stop_and_one_rumor(self):
        # GIVEN
        bus_driver_spec = 'bus-stop-a;rumor1'

        # WHEN
        bus_drivers = BusDriversParserImpl().parse([bus_driver_spec])

        # THEN
        self.__assert_has_circular_bus_route_with_one_stop(bus_drivers)
        self.assertEqual(len(bus_drivers[0].get_rumors()), 1)

    def test_parse__with_multiple_drivers_with_different_bus_stop_and_rumor(
            self):
        # GIVEN
        bus_driver_specs = ['bus-stop-a;rumor1', 'bus-stop-b;rumor2']

        # WHEN
        bus_drivers = BusDriversParserImpl().parse(bus_driver_specs)

        # THEN
        self.__assert_bus_stops_are_not_same(bus_drivers)

        self.assertNotEqual(
            bus_drivers[0].get_rumors(), bus_drivers[1].get_rumors()
        )

    def test_parse__with_multiple_drivers_with_a_common_bus_stop(self):
        # GIVEN
        bus_driver_specs = ['bus-stop-a;rumor1', 'bus-stop-a;rumor2']

        # WHEN
        bus_drivers = BusDriversParserImpl().parse(bus_driver_specs)

        # THEN
        self.__assert_bus_stops_are_same(bus_drivers)

    def __assert_has_circular_bus_route_with_one_stop(self, bus_drivers):
        self.assertEquals(len(bus_drivers), 1)
        bus_stop = bus_drivers[0].get_current_bus_stop()
        next_bus_stop = bus_drivers[0].drive_to_next_bus_stop()
        self.assertEqual(bus_stop, next_bus_stop)

    def __assert_bus_stops_are_not_same(self, bus_drivers):
        self.assertEqual(len(bus_drivers), 2)
        driver1_stop1 = bus_drivers[0].get_current_bus_stop()
        driver2_stop1 = bus_drivers[1].get_current_bus_stop()
        self.assertNotEqual(driver1_stop1, driver2_stop1)

    def assert_bus_stop_are_same(self, bus_drivers):
        driver1_stop = bus_driver[0].get_current_bus_stop()
        driver2_stop = bus_driver[1].get_current_bus_stop()
        self.assertEqual(driver1_stop, driver2_stop)

