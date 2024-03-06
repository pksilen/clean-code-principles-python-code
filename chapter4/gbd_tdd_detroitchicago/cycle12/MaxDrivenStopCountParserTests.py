class MaxDrivenStopCountParserTests(unittest.TestCase):
    def test_parse__when_it_succeeds(self):
        # GIVEN
        max_driven_stop_count_as_str = '2'

        # WHEN
        max_driven_stop_count = MaxDrivenStopCountParserImpl().parse(
            max_driven_stop_count_as_str
        )

        # THEN
        self.assertEqual(max_driven_stop_count, 2)