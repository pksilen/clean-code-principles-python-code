import unittest
from unittest.mock import Mock

from GossipingBusDrivers import GossipingBusDrivers
from Rumor import Rumor


class GossipingBusDriversTests(unittest.TestCase):
    rumor1 = Rumor()
    rumor2 = Rumor()
    all_rumors = {rumor1, rumor2}

    def setUp(self):
        self.bus_driver_mock1 = Mock()
        self.bus_driver_mock2 = Mock()
        self.bus_stop_mock1 = Mock()
        self.bus_stop_mock2 = Mock()
        self.bus_stop_mock3 = Mock()

    def test_drive_until_all_rumors_shared__after_one_stop(self):
        # GIVEN
        self.bus_driver_mock1.drive_to_next_bus_stop.return_value = (
            self.bus_stop_mock1
        )

        self.bus_driver_mock2.drive_to_next_bus_stop.return_value = (
            self.bus_stop_mock1
        )

        self.bus_driver_mock1.get_rumors.return_value = self.all_rumors
        self.bus_driver_mock2.get_rumors.return_value = self.all_rumors

        gossiping_bus_drivers = GossipingBusDrivers(
            [self.bus_driver_mock1, self.bus_driver_mock2]
        )

        # WHEN
        all_rumors_were_shared = (
            gossiping_bus_drivers.drive_until_all_rumors_shared(100)
        )

        # THEN
        self.assertTrue(all_rumors_were_shared)
        self.bus_stop_mock1.share_rumors_with_drivers.assert_called_once()

    def test_drive_until_all_rumors_shared__after_two_stops(self):
        # GIVEN
        bus_stop_mocks = [
            self.bus_stop_mock1,
            self.bus_stop_mock2,
            self.bus_stop_mock3,
        ]

        self.bus_driver_mock1.drive_to_next_bus_stop.side_effect = [
            self.bus_stop_mock1,
            self.bus_stop_mock3,
        ]

        self.bus_driver_mock2.drive_to_next_bus_stop.side_effect = [
            self.bus_stop_mock2,
            self.bus_stop_mock3,
        ]

        self.bus_driver_mock1.get_rumors.side_effect = [
            {self.rumor1},
            {self.rumor1},
            self.all_rumors,
        ]

        self.bus_driver_mock2.get_rumors.side_effect = [
            {self.rumor2},
            {self.rumor2},
            self.all_rumors,
        ]

        gossiping_bus_drivers = GossipingBusDrivers(
            [self.bus_driver_mock1, self.bus_driver_mock2]
        )

        # WHEN
        all_rumors_were_shared = (
            gossiping_bus_drivers.drive_until_all_rumors_shared(100)
        )

        # THEN
        self.assertTrue(all_rumors_were_shared)

        for bus_stop_mock in bus_stop_mocks:
            bus_stop_mock.share_rumors_with_drivers.assert_called_once()

    def test_drive_until_all_rumors_shared__when_rumors_are_not_shared(self):
        # GIVEN
        bus_stop_mocks = [self.bus_stop_mock1, self.bus_stop_mock2]

        self.bus_driver_mock1.drive_to_next_bus_stop.return_value = (
            self.bus_stop_mock1
        )

        self.bus_driver_mock2.drive_to_next_bus_stop.return_value = (
            self.bus_stop_mock2
        )

        self.bus_driver_mock1.get_rumors.return_value = {self.rumor1}
        self.bus_driver_mock2.get_rumors.return_value = {self.rumor2}

        gossiping_bus_drivers = GossipingBusDrivers(
            [self.bus_driver_mock1, self.bus_driver_mock2]
        )

        max_driven_stop_count = 2

        # WHEN
        all_rumors_were_shared = (
            gossiping_bus_drivers.drive_until_all_rumors_shared(
                max_driven_stop_count
            )
        )

        # THEN
        self.assertFalse(all_rumors_were_shared)

        for bus_stop_mock in bus_stop_mocks:
            self.assertEqual(
                bus_stop_mock.share_rumors_with_drivers.call_count, 2
            )
