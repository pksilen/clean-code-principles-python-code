from model.errors.TripBookingServiceError import TripBookingServiceError
from model.services.reservation.ReservationService import ReservationService


class RentalCarReservationService(ReservationService):
    class ReserveCarError(TripBookingServiceError):
        pass

    def reserve_car(self, ...) -> str:
        pass