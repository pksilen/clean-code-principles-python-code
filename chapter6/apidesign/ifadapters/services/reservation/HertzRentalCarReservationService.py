from model.services.reservation.RentalCarReservationService import \
    RentalCarReservationService


class HertzRentalCarReservationService(RentalCarReservationService):
    def reserve_car(self, ...) -> str:
        # ...

    def cancel_reservation(self, id_: str) -> None:
        # ...