import os
import sys

from KafkaClient import KafkaClient


def get_environ_var(name: str) -> str:
    return (
        os.environ.get(name)
        or f'Environment variable {name} is not defined'
    )


def main():
    kafka_client = KafkaClient(get_environ_var('KAFKA_HOST'))

    try:
        kafka_client.try_create_topic(
            get_environ_var('KAFKA_TOPIC'),
            num_partitions=3,
            replication_factor=2,
            retention_in_secs=5 * 60,
            retention_in_gb=100,
        )
    except KafkaClient.CreateTopicError:
        sys.exit(1)


if __name__ == '__main__':
    main()