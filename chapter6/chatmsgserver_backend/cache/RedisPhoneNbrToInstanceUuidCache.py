from PhoneNbrToInstanceUuidCache import PhoneNbrToInstanceUuidCache
from redis import Redis, RedisError


class RedisPhoneNbrToInstanceUuidCache(PhoneNbrToInstanceUuidCache):
    def __init__(self, redis_client: Redis):
        self.__redis_client = redis_client

    def retrieve_instance_uuid(
        self, phone_number: str | None
    ) -> str | None:
        if phone_number:
            try:
                return self.__redis_client.hget(
                    'phoneNbrToInstanceUuidMap', phone_number
                )
            except RedisError:
                pass

        return None

    def try_store(self, phone_number: str, instance_uuid: str) -> None:
        try:
            self.__redis_client.hset(
                'phoneNbrToInstanceUuidMap', phone_number, instance_uuid
            )
        except RedisError:
            raise self.Error()

    def try_remove(self, phone_number: str) -> None:
        try:
            self.__redis_client.hdel(
                'phoneNbrToInstanceUuidMap', [phone_number]
            )
        except RedisError:
            raise self.Error()
