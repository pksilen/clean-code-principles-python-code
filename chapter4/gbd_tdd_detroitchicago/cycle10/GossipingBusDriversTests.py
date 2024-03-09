import unittest

from BusDriverImpl import BusDriverImpl
from BusStopImpl import BusStopImpl
from CircularBusRoute import CircularBusRoute
from GossipingBusDrivers import GossipingBusDrivers
from Rumor import Rumor


class GossipingBusDriversTests(unittest.TestCase):
    rumor1 = Rumor()
    rumor2 = Rumor()
    all_rumors = {rumor1, rumor2}

    def test_drive_until_all_rumors_shared__after_one_stop(self):
        # GIVEN
        bus_stop = BusStopImpl()
        bus_route = CircularBusRoute([bus_stop])
        bus_driver1 = BusDriverImpl(bus_route, {self.rumor1})
        bus_driver2 = BusDriverImpl(bus_route, {self.rumor2})

        gossiping_bus_drivers = GossipingBusDrivers([bus_driver1, bus_driver2])

        # WHEN
        all_rumors_were_shared = (
            gossiping_bus_drivers.drive_until_all_rumors_shared()
        )

        # THEN
        self.assertTrue(all_rumors_were_shared)
        self.assertEqual(bus_driver1.get_rumors(), self.all_rumors)
        self.assertEqual(bus_driver2.get_rumors(), self.all_rumors)

    def test_drive_until_all_rumors_shared__after_two_stops(self):
        # GIVEN
        bus_stop_a = BusStopImpl()
        bus_stop_b = BusStopImpl()
        bus_stop_c = BusStopImpl()
        bus_route1 = CircularBusRoute([bus_stop_a, bus_stop_c])
        bus_route2 = CircularBusRoute([bus_stop_b, bus_stop_c])
        bus_driver1 = BusDriverImpl(bus_route1, {self.rumor1})
        bus_driver2 = BusDriverImpl(bus_route2, {self.rumor2})
        gossiping_bus_drivers = GossipingBusDrivers([bus_driver1, bus_driver2])

        # WHEN
        all_rumors_were_shared = (
            gossiping_bus_drivers.drive_until_all_rumors_shared()
        )

        # THEN
        self.assertTrue(all_rumors_were_shared)
        self.assertEqual(bus_driver1.get_rumors(), self.all_rumors)
        self.assertEqual(bus_driver2.get_rumors(), self.all_rumors)
