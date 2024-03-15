from typing import Protocol

from entities.Trip import Trip
from errors.TripBookingServiceError import TripBookingServiceError


class TripRepository(Protocol):
    class Error(TripBookingServiceError):
        pass

    def save(self, trip: Trip) -> None:
        pass

    def update(self, trip: Trip) -> None:
        pass
