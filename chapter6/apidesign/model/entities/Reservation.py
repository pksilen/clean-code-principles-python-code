from typing import Protocol

from model.errors.TripBookingServiceError import TripBookingServiceError


class Reservation(Protocol):
    class MakeError(TripBookingServiceError):
        pass

    class AlreadyReservedError(MakeError):
        pass

    def make(self) -> None:
        pass

    class CancelError(TripBookingServiceError):
        pass

    def cancel(self) -> None:
        pass
