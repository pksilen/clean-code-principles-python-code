from model.services.reservation.FlightReservationService import \
    FlightReservationService


class GalileoFlightReservationService(FlightReservationService):
    def reserve_flight(self, ...) -> str:
        # ...

    def cancel_reservation(self, id_: str) -> None:
        # ...