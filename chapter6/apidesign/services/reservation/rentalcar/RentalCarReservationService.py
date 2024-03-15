from errors.TripBookingServiceError import TripBookingServiceError
from services.reservation.ReservationService import ReservationService


class RentalCarReservationService(ReservationService):
    class ReserveCarError(TripBookingServiceError):
        pass

    def reserve_car(self, ...) -> None:
        pass