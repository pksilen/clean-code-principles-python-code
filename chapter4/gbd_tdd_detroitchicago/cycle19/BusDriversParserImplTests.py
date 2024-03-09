import unittest

from BusDriver import BusDriver
from BusDriversParserImpl import BusDriversParserImpl


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
        self,
    ):
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

    def test_parse__with_multiple_drivers_and_a_common_rumor(
        self,
    ):
        # GIVEN
        bus_driver_specs = ['bus-stop-a;rumor1', 'bus-stop-b;rumor1']

        # WHEN
        bus_drivers = BusDriversParserImpl().parse(bus_driver_specs)

        # THEN
        self.assertEqual(
            bus_drivers[0].get_rumors(), bus_drivers[1].get_rumors()
        )

    def test_parse__with_multiple_drivers_and_multiple_bus_stops_where_first_is_common(
        self,
    ):
        # GIVEN
        bus_driver_specs = [
            'bus-stop-a,bus-stop-b;rumor1',
            'bus-stop-a,bus-stop-c;rumor2',
        ]

        # WHEN
        bus_drivers = BusDriversParserImpl().parse(bus_driver_specs)

        # THEN
        self.__assert_only_first_bus_stop_is_same(bus_drivers)

    def test_parse__with_multiple_drivers_and_multiple_rumors(self):
        # GIVEN
        bus_driver_specs = [
            'bus-stop-a;rumor1,rumor2,rumor3',
            'bus-stop-b;rumor1,rumor3',
        ]

        # WHEN
        bus_drivers = BusDriversParserImpl().parse(bus_driver_specs)

        # THEN
        self.__assert_rumors_differ_by_one(bus_drivers)

    def __assert_has_circular_bus_route_with_one_stop(
        self, bus_drivers: list[BusDriver]
    ):
        self.assertEqual(len(bus_drivers), 1)
        bus_stop = bus_drivers[0].get_current_bus_stop()
        next_bus_stop = bus_drivers[0].drive_to_next_bus_stop()
        self.assertEqual(bus_stop, next_bus_stop)

    def __assert_bus_stops_are_not_same(self, bus_drivers: list[BusDriver]):
        self.assertEqual(len(bus_drivers), 2)
        driver1_stop1 = bus_drivers[0].get_current_bus_stop()
        driver2_stop1 = bus_drivers[1].get_current_bus_stop()
        self.assertNotEqual(driver1_stop1, driver2_stop1)

    def __assert_bus_stops_are_same(self, bus_drivers: list[BusDriver]):
        driver1_stop = bus_drivers[0].get_current_bus_stop()
        driver2_stop = bus_drivers[1].get_current_bus_stop()
        self.assertEqual(driver1_stop, driver2_stop)

    def __assert_only_first_bus_stop_is_same(
        self, bus_drivers: list[BusDriver]
    ):
        driver1_stop1 = bus_drivers[0].get_current_bus_stop()
        driver2_stop1 = bus_drivers[1].get_current_bus_stop()
        self.assertEqual(driver1_stop1, driver2_stop1)

        driver1_stop2 = bus_drivers[0].drive_to_next_bus_stop()
        driver2_stop2 = bus_drivers[1].drive_to_next_bus_stop()
        self.assertNotEqual(driver1_stop2, driver2_stop2)

    def __assert_rumors_differ_by_one(self, bus_drivers: list[BusDriver]):
        self.assertEqual(len(bus_drivers[0].get_rumors()), 3)
        self.assertEqual(len(bus_drivers[1].get_rumors()), 2)

        rumor_diff = (
            bus_drivers[0].get_rumors().difference(bus_drivers[1].get_rumors())
        )

        self.assertEqual(len(rumor_diff), 1)
