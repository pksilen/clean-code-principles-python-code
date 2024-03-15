from dependency_injector.wiring import Provide

from model.dtos.InputRentalCarReservation import InputRentalCarReservation
from model.entities.AbstractReservation import AbstractReservation
from model.services.reservation.RentalCarReservationService import \
    RentalCarReservationService


class RentalCarReservation(AbstractReservation):
    __rental_car_reservation_service: RentalCarReservationService = Provide[
        'rental_car_reservation_service'
    ]

    def __init__(self, ...):
        super().__init__(...)
        # Set rental car reservation related attributes ...

    @staticmethod
    def create_from(
        input_rental_car_reservation: InputRentalCarReservation,
    ) -> 'RentalCarReservation':
        pass

    def make(self) -> None:
        self._assert_is_not_reserved()

        try:
            self.id = self.__rental_car_reservation_service.reserve_car(...)
        except self.__rental_car_reservation_service.ReserveCarError as error:
            raise self.MakeError(error)

    def cancel(self) -> None:
        self._cancel_using(self.__rental_car_reservation_service)
