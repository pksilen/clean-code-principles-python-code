import unittest
from unittest.mock import patch, Mock

from GossipingBusDrivers import GossipingBusDrivers
from Rumor import Rumor


class GossipingBusDriversTests(unittest.TestCase):
    rumor1 = Rumor()
    rumor2 = Rumor()
    all_rumors = {rumor1, rumor2}

    @patch('BusStopImpl.__new__')
    @patch('BusDriverImpl.__new__')
    @patch('BusDriverImpl.__new__')
    def test_drive_until_all_rumors_shared__after_one_stop(
        self,
        bus_driver_mock1: Mock,
        bus_driver_mock2: Mock,
        bus_stop_mock: Mock,
    ):
        # GIVEN
        bus_driver_mock1.drive_to_next_bus_stop.return_value = bus_stop_mock

        bus_driver_mock2.drive_to_next_bus_stop.return_value = bus_stop_mock

        bus_driver_mock1.get_rumors.return_value = self.all_rumors
        bus_driver_mock2.get_rumors.return_value = self.all_rumors

        gossiping_bus_drivers = GossipingBusDrivers(
            [bus_driver_mock1, bus_driver_mock2]
        )

        # WHEN
        all_rumors_were_shared = (
            gossiping_bus_drivers.drive_until_all_rumors_shared()
        )

        # THEN
        self.assertTrue(all_rumors_were_shared)
        bus_stop_mock.share_rumors_with_drivers.assert_called_once()

    @patch('BusStopImpl.__new__')
    @patch('BusStopImpl.__new__')
    @patch('BusStopImpl.__new__')
    @patch('BusDriverImpl.__new__')
    @patch('BusDriverImpl.__new__')
    def test_drive_until_all_rumors_shared__after_two_stops(
        self,
        bus_driver_mock1: Mock,
        bus_driver_mock2: Mock,
        bus_stop_mock1: Mock,
        bus_stop_mock2: Mock,
        bus_stop_mock3: Mock,
    ):
        # GIVEN
        bus_stop_mocks = [bus_stop_mock1, bus_stop_mock2, bus_stop_mock3]

        bus_driver_mock1.drive_to_next_bus_stop.side_effect = [
            bus_stop_mock1,
            bus_stop_mock3,
        ]

        bus_driver_mock2.drive_to_next_bus_stop.side_effect = [
            bus_stop_mock2,
            bus_stop_mock3,
        ]

        bus_driver_mock1.get_rumors.side_effect = [
            {self.rumor1},
            {self.rumor1},
            self.all_rumors,
        ]

        bus_driver_mock2.get_rumors.side_effect = [
            {self.rumor2},
            {self.rumor2},
            self.all_rumors,
        ]

        gossiping_bus_drivers = GossipingBusDrivers(
            [bus_driver_mock1, bus_driver_mock2]
        )

        # WHEN
        all_rumors_were_shared = (
            gossiping_bus_drivers.drive_until_all_rumors_shared()
        )

        # THEN
        self.assertTrue(all_rumors_were_shared)

        for bus_stop_mock in bus_stop_mocks:
            bus_stop_mock.share_rumors_with_drivers.assert_called_once()
