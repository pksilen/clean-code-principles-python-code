
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

    @patch('CircularBusRoute.__new__')
    def test_set_rumors(self, bus_route_mock: Mock):
        # GIVEN
        rumor3 = Rumor()
        rumor4 = Rumor()

        bus_driver = BusDriverImpl(
            bus_route_mock, {self.rumor1, self.rumor2}
        )

        # WHEN
        bus_driver.set_rumors({rumor3, rumor4})

        # THEN
        self.assertEqual(bus_driver.get_rumors(), {rumor3, rumor4})

    @patch('BusStopImpl.__new__')
    @patch('BusStopImpl.__new__')
    @patch('CircularBusRoute.__new__')
    def test_drive_to_next_bus_stop(
            self,
            bus_route_mock: Mock,
            bus_stop_a_mock: Mock,
            bus_stop_b_mock: Mock,
    ):
        # GIVEN
        bus_route_mock.get_first_bus_stop.return_value = bus_stop_a_mock
        bus_route_mock.get_next_bus_stop.return_value = bus_stop_b_mock
        bus_driver = BusDriverImpl(bus_route_mock, set())

        # WHEN
        bus_driver.drive_to_next_bus_stop()

        # THEN
        bus_stop_a_mock.remove.assert_called_with(bus_driver)
        bus_stop_b_mock.add.assert_called_with(bus_driver)

        self.assertEqual(
            bus_driver.get_current_bus_stop(), bus_stop_b_mock
        )