import unittest
from unittest.mock import Mock

from BusDriverImpl import BusDriverImpl
from Rumor import Rumor


class BusDriverImplTests(unittest.TestCase):
    rumor1 = Rumor()
    rumor2 = Rumor()

    def setUp(self):
        self.bus_route_mock = Mock()

    def test_drive_to_next_bus_stop(self):
        # GIVEN
        bus_stop_mock1 = Mock()
        bus_stop_mock2 = Mock()
        self.bus_route_mock.get_first_bus_stop.return_value = bus_stop_mock1
        self.bus_route_mock.get_next_bus_stop.return_value = bus_stop_mock2
        bus_driver = BusDriverImpl(self.bus_route_mock, set())

        # WHEN
        bus_driver.drive_to_next_bus_stop()

        # THEN
        bus_stop_mock1.remove.assert_called_with(bus_driver)
        bus_stop_mock2.add.assert_called_with(bus_driver)

        self.assertEqual(bus_driver.get_current_bus_stop(), bus_stop_mock2)

    def test_get_rumors(self):
        # GIVEN
        bus_driver = BusDriverImpl(
            self.bus_route_mock, {self.rumor1, self.rumor2}
        )

        # WHEN
        rumors = bus_driver.get_rumors()

        # THEN
        self.assertEqual(rumors, {self.rumor1, self.rumor2})

    def test_set_rumors(self):
        # GIVEN
        rumor3 = Rumor()
        rumor4 = Rumor()

        bus_driver = BusDriverImpl(
            self.bus_route_mock, {self.rumor1, self.rumor2}
        )

        # WHEN
        bus_driver.set_rumors({rumor3, rumor4})

        # THEN
        self.assertEqual(bus_driver.get_rumors(), {rumor3, rumor4})
