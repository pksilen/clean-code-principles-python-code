import unittest

from BusDriverImpl import BusDriverImpl
from BusStopImpl import BusStopImpl
from CircularBusRoute import CircularBusRoute
from Rumor import Rumor


class BusStopImplTests(unittest.TestCase):
    def test_share_rumors_with_drivers(
        self,
    ):
        # GIVEN
        rumor1 = Rumor()
        rumor2 = Rumor()
        rumor3 = Rumor()
        all_rumors = {rumor1, rumor2, rumor3}

        bus_driver1 = BusDriverImpl(
            CircularBusRoute([BusStopImpl()]), {rumor1, rumor2}
        )

        bus_driver2 = BusDriverImpl(
            CircularBusRoute([BusStopImpl()]), {rumor2}
        )

        bus_driver3 = BusDriverImpl(
            CircularBusRoute([BusStopImpl()]), {rumor2, rumor3}
        )

        bus_drivers = [bus_driver1, bus_driver2, bus_driver3]

        bus_stop = BusStopImpl()
        bus_stop.add(bus_driver1)
        bus_stop.add(bus_driver2)
        bus_stop.add(bus_driver3)

        # WHEN
        bus_stop.share_rumors_with_drivers()

        # THEN
        for bus_driver in bus_drivers:
            self.assertEqual(bus_driver.get_rumors(), all_rumors)

    def test_add(self):
        # GIVEN
        bus_stop = BusStopImpl()
        bus_driver = BusDriverImpl(CircularBusRoute([BusStopImpl()]), set())

        # WHEN
        bus_stop.add(bus_driver)

        # THEN
        self.assertEqual(bus_stop.get_bus_driver_count(), 1)

    def test_remove(self):
        # GIVEN
        bus_stop = BusStopImpl()
        bus_driver = BusDriverImpl(CircularBusRoute([BusStopImpl()]), set())
        bus_stop.add(bus_driver)

        # WHEN
        bus_stop.remove(bus_driver)

        # THEN
        self.assertEqual(bus_stop.get_bus_driver_count(), 0)
