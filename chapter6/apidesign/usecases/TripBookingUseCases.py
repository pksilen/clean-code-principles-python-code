from typing import Protocol

from dtos.InputRentalCarReservation import InputRentalCarReservation
from dtos.InputTrip import InputTrip
from dtos.OutputRentalCarReservation import OutputRentalCarReservation
from dtos.OutputTrip import OutputTrip


class TripBookingUseCases(Protocol):
    def book_trip(self, input_trip: InputTrip) -> OutputTrip:
        pass

    def add_rental_car_reservation(
        self,
        trip_id: str,
        input_rental_car_reservation: InputRentalCarReservation,
    ) -> OutputRentalCarReservation:
        pass
