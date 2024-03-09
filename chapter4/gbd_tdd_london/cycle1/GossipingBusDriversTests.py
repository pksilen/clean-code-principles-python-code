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
        self.assertEqual(bus_stop_mock.share_rumors_with_drivers.call_count, 2)
