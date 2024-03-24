from model.entities.Trip import Trip
from model.repositories.TripRepository import TripRepository


class MongoDbTripRepository(TripRepository):
    def save(self, trip: Trip) -> None:
        # ...

    def find(self, id_: str) -> Trip | None:
        # ...

    def update(self, trip: Trip) -> None:
        # ...
