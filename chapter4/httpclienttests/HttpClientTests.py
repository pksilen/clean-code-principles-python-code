import json
from unittest import TestCase
from unittest.mock import Mock, patch

import requests
from HttpClient import HttpClient

URL = 'https://localhost:8080/'
DICT = {'test': 'test'}


@patch('requests.get')
class HttpClientTests(TestCase):
    def setUp(self):
        self.__response_mock = Mock()

    def test_try_fetch_resource__when_fetch_succeeds(
        self, requests_get_mock: Mock
    ):
        # GIVEN
        requests_get_mock.return_value = self.__response_mock
        self.__response_mock.json.return_value = DICT

        # WHEN
        dict_ = HttpClient().try_fetch_resource(URL)

        # THEN
        requests_get_mock.assert_called_once_with(URL, timeout=60)
        self.assertDictEqual(dict_, DICT)

    def test_try_fetch_resource__when_json_parse_fails(
        self, requests_get_mock: Mock
    ):
        # GIVEN
        requests_get_mock.return_value = self.__response_mock
        self.__response_mock.json.side_effect = requests.JSONDecodeError(
            'JSON decode error', json.dumps(DICT), 1
        )

        # WHEN
        self.assertRaises(
            HttpClient.Error, HttpClient().try_fetch_resource, URL
        )

        # THEN
        requests_get_mock.assert_called_once_with(URL, timeout=60)

    def test_try_fetch_resource__when_response_has_error(
        self, requests_get_mock: Mock
    ):
        # GIVEN
        requests_get_mock.return_value = self.__response_mock
        self.__response_mock.raise_for_status.side_effect = requests.HTTPError()

        # WHEN
        self.assertRaises(
            HttpClient.Error, HttpClient().try_fetch_resource, URL
        )

        # THEN
        requests_get_mock.assert_called_once_with(URL, timeout=60)

    def test_try_fetch_resource__when_remote_connection_fails(
        self, requests_get_mock: Mock
    ):
        # GIVEN
        requests_get_mock.side_effect = requests.ConnectionError()

        # WHEN
        self.assertRaises(
            HttpClient.Error, HttpClient().try_fetch_resource, URL
        )

        # THEN
        requests_get_mock.assert_called_once_with(URL, timeout=60)
