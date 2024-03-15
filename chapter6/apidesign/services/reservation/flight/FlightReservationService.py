from errors.TripBookingServiceError import TripBookingServiceError
from services.reservation.ReservationService import ReservationService


class FlightReservationService(ReservationService):
    class ReserveFlightError(TripBookingServiceError):
        pass

    def reserve_flight(self, ...) -> None:
        pass