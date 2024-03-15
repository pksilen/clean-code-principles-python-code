from errors.TripBookingServiceError import TripBookingServiceError
from services.reservation.ReservationService import ReservationService


class HotelReservationService(ReservationService):
    class ReserveHotelError(TripBookingServiceError):
        pass

    def reserve_hotel(self, ...) -> None:
        pass