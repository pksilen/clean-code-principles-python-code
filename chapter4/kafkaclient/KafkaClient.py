from confluent_kafka import KafkaError, KafkaException
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

from DataExporterError import DataExporterError


class KafkaClient:
    def __init__(self, kafka_host: str):
        self.__admin_client = AdminClient(
            {'bootstrap.servers': kafka_host}
        )

    class CreateTopicError(DataExporterError):
        pass

    def try_create_topic(
        self,
        name: str,
        num_partitions: int,
        replication_factor: int,
        retention_in_secs: int,
        retention_in_gb: int
    ):
        topic = NewTopic(
            name,
            num_partitions,
            replication_factor,
            config={
                'retention.ms': str(retention_in_secs * 1000),
                'retention.bytes': str(retention_in_gb * pow(10, 9))
            }
        )

        try:
            topic_name_to_creation_future = (
                self.__admin_client.create_topics([topic])
            )

            topic_name_to_creation_future[name].result()
        except KafkaException as error:
            if error.args[0].code() != KafkaError.TOPIC_ALREADY_EXISTS:
                raise self.CreateTopicError(error)