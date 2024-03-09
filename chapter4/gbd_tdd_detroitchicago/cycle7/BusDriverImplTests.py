import unittest

from BusDriverImpl import BusDriverImpl
from BusStopImpl import BusStopImpl
from CircularBusRoute import CircularBusRoute
from Rumor import Rumor


class BusDriverImplTests(unittest.TestCase):
    rumor1 = Rumor()
    rumor2 = Rumor()

    def test_get_rumors(self):
        # GIVEN
        bus_driver = BusDriverImpl(
            CircularBusRoute([BusStopImpl()]), {self.rumor1, self.rumor2}
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
            CircularBusRoute([BusStopImpl()]), {self.rumor1, self.rumor2}
        )

        # WHEN
        bus_driver.set_rumors({rumor3, rumor4})

        # THEN
        self.assertEqual(bus_driver.get_rumors(), {rumor3, rumor4})
