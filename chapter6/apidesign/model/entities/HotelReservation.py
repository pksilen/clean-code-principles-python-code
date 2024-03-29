from dependency_injector.wiring import Provide

from model.entities.AbstractReservation import AbstractReservation
from model.services.reservation.HotelReservationService import \
    HotelReservationService


class HotelReservation(AbstractReservation):
    __hotel_reservation_service: HotelReservationService = Provide['hotel_reservation_service']

    def __init__(self, ...):
        super().__init__()

    def make(self) -> None:
        self._assert_is_not_reserved()

        try:
            self.id = self.__hotel_reservation_service.reserve_hotel(...)
        except self.__hotel_reservation_service.ReserveHotelError as error:
            raise self.MakeError(error)

    def cancel(self) -> None:
        self._cancel_using(self.__hotel_reservation_service)