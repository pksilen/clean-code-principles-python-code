
class BusDriverImplTests(unittest.TestCase):
    rumor1 = Rumor()
    rumor2 = Rumor()

    @patch('CircularBusRoute.__new__')
    def test_get_rumors(self, bus_route_mock: Mock):
        # GIVEN
        bus_driver = BusDriverImpl(
            bus_route_mock, {self.rumor1, self.rumor2}
        )

        # WHEN
        rumors = bus_driver.get_rumors()

        # THEN
        self.assertEqual(rumors, {self.rumor1, self.rumor2})