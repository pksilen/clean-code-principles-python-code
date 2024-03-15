from entities.Trip import Trip
from repositories.TripRepository import TripRepository


class MongoDbTripRepository(TripRepository):
    def save(self, trip: Trip) -> None:
        # ...

    def update(self, trip: Trip) -> None:
        # ...
