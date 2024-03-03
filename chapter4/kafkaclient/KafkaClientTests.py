from unittest import TestCase
from unittest.mock import Mock, patch

from confluent_kafka import KafkaError, KafkaException
from KafkaClient import KafkaClient


@patch('asyncio.Future')
@patch('KafkaClient.NewTopic')
@patch('KafkaClient.AdminClient')
class KafkaClientTests(TestCase):
    def test_try_create_topic__when_create_succeeds(
        self,
        admin_client_class_mock: Mock,
        new_topic_class_mock: Mock,
        future_class_mock: Mock,
    ):
        # GIVEN
        self.__set_up(admin_client_class_mock, future_class_mock)

        # WHEN
        self.kafka_client.try_create_topic('test', **self.topic_params)

        # THEN
        self.__assert_mock_calls(
            admin_client_class_mock, new_topic_class_mock
        )

        self.topic_creation_future_mock.result.assert_called_once()

    def test_try_create_topic__when_create_fails(
        self,
        admin_client_class_mock: Mock,
        new_topic_class_mock: Mock,
        future_class_mock: Mock,
    ):
        # GIVEN
        self.__set_up(admin_client_class_mock, future_class_mock)
        self.topic_creation_future_mock.result.side_effect = KafkaException(KafkaError(1))

        # WHEN
        try:
            self.kafka_client.try_create_topic('test', **self.topic_params)
            self.fail('KafkaClient.CreateTopicError should have been raised')
        except KafkaClient.CreateTopicError:
            pass

        # THEN
        self.__assert_mock_calls(
            admin_client_class_mock, new_topic_class_mock
        )

    def test_try_create_topic__when_topic_exists(
            self,
            admin_client_class_mock: Mock,
            new_topic_class_mock: Mock,
            future_class_mock: Mock,
    ):
        # GIVEN
        self.__set_up(admin_client_class_mock, future_class_mock)
        self.topic_creation_future_mock.result.side_effect = (
            KafkaException(KafkaError(KafkaError.TOPIC_ALREADY_EXISTS))
        )

        # WHEN
        self.kafka_client.try_create_topic('test', **self.topic_params)

        # THEN
        self.__assert_mock_calls(
            admin_client_class_mock, new_topic_class_mock
        )

    def __set_up(
        self,
        admin_client_class_mock: Mock,
        future_class_mock: Mock,
    ) -> None:
        # GIVEN
        self.admin_client_mock = admin_client_class_mock.return_value
        self.topic_creation_future_mock = future_class_mock.return_value

        self.admin_client_mock.create_topics.return_value = {
            'test': self.topic_creation_future_mock
        }

        self.topic_params = {
            'num_partitions': 3,
            'replication_factor': 2,
            'retention_in_secs': 5 * 60,
            'retention_in_gb': 100,
        }

        self.kafka_client = KafkaClient('localhost:9092')

    def __assert_mock_calls(
        self, admin_client_class_mock: Mock, new_topic_class_mock: Mock
    ):
        admin_client_class_mock.assert_called_once_with(
            {'bootstrap.servers': 'localhost:9092'}
        )

        new_topic_class_mock.assert_called_once_with(
            'test',
            3,
            2,
            config={
                'retention.ms': str(5 * 60 * 1000),
                'retention.bytes': str(100 * pow(10, 9)),
            },
        )

        self.admin_client_mock.create_topics.assert_called_once_with(
            [new_topic_class_mock.return_value]
        )
