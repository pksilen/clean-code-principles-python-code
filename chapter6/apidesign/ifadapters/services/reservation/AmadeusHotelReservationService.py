from model.services.reservation.HotelReservationService import \
    HotelReservationService


class AmadeusHotelReservationService(HotelReservationService):
    def reserve_hotel(self, ...) -> str:
        # ...

    def cancel_reservation(self, id_: str) -> None:
        # ...