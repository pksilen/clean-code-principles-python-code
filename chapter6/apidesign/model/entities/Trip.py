from model.dtos.InputTrip import InputTrip
from model.entities.FlightReservation import FlightReservation
from model.entities.HotelReservation import HotelReservation
from model.entities.RentalCarReservation import RentalCarReservation
from model.entities.Reservation import Reservation


class Trip:
    def __init__(self, reservations: list[Reservation], ...):
        self.__reservations = reservations

    @staticmethod
    def create_from(input_trip: InputTrip) -> 'Trip':
        reservations = []

        for flight_reservation in input_trip.flight_reservations:
            reservations.append(FlightReservation(...))

        for hotel_reservation in input_trip.hotel_reservations:
            reservations.append(HotelReservation(...))

        for rental_car_reservation in input_trip.rental_car_reservations:
            reservations.append(RentalCarReservation(...))

        return Trip(reservations, ...)

    def make_reservations(self) -> None:
        try:
            for reservation in self.__reservations:
                reservation.make()
        except Reservation.MakeError as error:
            # We are inside a distributed transaction
            # Compensating actions
            self.cancel_reservations()
            raise error

    def cancel_reservations(self) -> None:
        # In production code, this loop cannot be forever but should be
        # replaced with more robust and complex error handling as described
        # earlier in first chapter when discussing distributed transactions
        while self.__reservations:
            try:
                for reservation in self.__reservations:
                    reservation.cancel()
                    self.__reservations.remove(reservation)
                    break
            except Reservation.CancelError:
                pass

    def add(self, reservation: Reservation) -> None:
        reservation.make()
        self.__reservations.append(reservation)

    def remove(self, reservation: Reservation) -> None:
        while True:
            try:
                reservation.cancel()
                break
            except reservation.CancelError:
                pass

        self.__reservations.remove(reservation)
