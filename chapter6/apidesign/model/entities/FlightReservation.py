from dependency_injector.wiring import Provide

from model.entities.AbstractReservation import AbstractReservation
from model.services.reservation.FlightReservationService import \
    FlightReservationService


class FlightReservation(AbstractReservation):
    __flight_reservation_service: FlightReservationService = Provide['flight_reservation_service']

    def __init__(self, ...):
        super().__init__(...)
        # Set flight reservation related attributes ...

    def make(self) -> None:
        self._assert_is_not_reserved()

        try:
            self.id = self.__flight_reservation_service.reserve_flight(...)
        except self.__flight_reservation_service.ReserveFlightError as error:
            raise self.MakeError(error)

    def cancel(self) -> None:
        self._cancel_using(self.__flight_reservation_service)