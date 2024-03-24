from model.errors.TripBookingServiceError import TripBookingServiceError
from model.services.reservation.ReservationService import ReservationService


class HotelReservationService(ReservationService):
    class ReserveHotelError(TripBookingServiceError):
        pass

    def reserve_hotel(self, ...) -> str:
        pass