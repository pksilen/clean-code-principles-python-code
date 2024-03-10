import unittest
from unittest.mock import Mock

from BusDriver import BusDriver
from BusStopImpl import BusStopImpl
from Rumor import Rumor


class BusStopImplTests(unittest.TestCase):
    def test_share_rumors_with_drivers(self):
        # GIVEN
        bus_driver_mock1 = Mock()
        bus_driver_mock2 = Mock()
        bus_driver_mock3 = Mock()
        bus_drivers = [bus_driver_mock1, bus_driver_mock2, bus_driver_mock3]

        rumor1 = Rumor()
        rumor2 = Rumor()
        rumor3 = Rumor()
        all_rumors = {rumor1, rumor2, rumor3}

        bus_driver_mock1.get_rumors.return_value = {rumor1, rumor2}
        bus_driver_mock2.get_rumors.return_value = {rumor2}
        bus_driver_mock3.get_rumors.return_value = {rumor2, rumor3}

        bus_stop = BusStopImpl()
        bus_stop.add(bus_driver_mock1)
        bus_stop.add(bus_driver_mock2)
        bus_stop.add(bus_driver_mock3)

        # WHEN
        bus_stop.share_rumors_with_drivers()

        # THEN
        self.__assert_rumors_are_set(all_rumors, bus_drivers)

    def __assert_rumors_are_set(
        self, all_rumors: set[Rumor], bus_driver_mocks: list[BusDriver]
    ):
        for bus_driver_mock in bus_driver_mocks:
            bus_driver_mock.set_rumors.assert_called_with(all_rumors)

    def test_share_rumors_with_drivers__when_driver_is_removed(self):
        # GIVEN
        bus_stop = BusStopImpl()
        bus_driver_mock = Mock()
        bus_stop.add(bus_driver_mock)

        # WHEN
        bus_stop.remove(bus_driver_mock)
        bus_stop.share_rumors_with_drivers()

        # THEN
        self.assertFalse(bus_driver_mock.set_rumors.called)
