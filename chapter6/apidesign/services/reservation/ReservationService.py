from typing import Protocol

from errors.TripBookingServiceError import TripBookingServiceError


class ReservationService(Protocol):
    class CancelReservationError(TripBookingServiceError):
        pass

    def cancel_reservation(self, id_: str) -> None:
        pass
