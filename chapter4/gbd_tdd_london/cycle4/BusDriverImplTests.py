import unittest

from BusDriverImpl import BusDriverImpl
from Rumor import Rumor


class BusDriverImplTests(unittest.TestCase):
    rumor1 = Rumor()
    rumor2 = Rumor()

    def test_get_rumors(self):
        # GIVEN
        bus_driver = BusDriverImpl({self.rumor1, self.rumor2})

        # WHEN
        rumors = bus_driver.get_rumors()

        # THEN
        self.assertEqual(rumors, {self.rumor1, self.rumor2})
