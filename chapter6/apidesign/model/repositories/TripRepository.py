from typing import Protocol

from model.entities.Trip import Trip
from model.errors.TripBookingServiceError import TripBookingServiceError


class TripRepository(Protocol):
    class Error(TripBookingServiceError):
        pass

    def save(self, trip: Trip) -> None:
        pass

    def update(self, trip: Trip) -> None:
        pass
