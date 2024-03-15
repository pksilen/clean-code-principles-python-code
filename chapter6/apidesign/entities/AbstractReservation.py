from entities.Reservation import Reservation
from services.reservation.ReservationService import ReservationService


class AbstractReservation(Reservation):
    def __init__(self, id_: str):
        self.__id = id_

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id_: str) -> None:
        self.__id = id_

    def _assert_is_not_reserved(self) -> None:
        if self.__id is not None:
            raise self.AlreadyReservedError()

    def _cancel_using(self, reservation_service: ReservationService) -> None:
        if self.__id is None:
            return

        try:
            reservation_service.cancel_reservation(self.__id)
            self.__id = None
        except reservation_service.CancelReservationError as error:
            raise self.CancelError(error)
