from dependency_injector.wiring import Provide
from fastapi import APIRouter

from model.dtos.InputRentalCarReservation import InputRentalCarReservation
from model.dtos.InputTrip import InputTrip
from model.dtos.OutputRentalCarReservation import OutputRentalCarReservation
from model.dtos.OutputTrip import OutputTrip
from model.usecases.TripBookingUseCases import TripBookingUseCases


class RestTripController:
    __trip_booking_use_cases: TripBookingUseCases = Provide['trip_use_cases']

    def __init__(self):
        self.__router = APIRouter()

        self.__router.add_api_route(
            '/trips/',
            self.book_trip,
            methods=['POST'],
            status_code=201,
            response_model=OutputTrip,
        )

        self.__router.add_api_route(
            '/trips/{trip_id}/rental-car-reservations',
            self.add_rental_car_reservation,
            methods=['POST'],
            status_code=201,
            response_model=OutputRentalCarReservation,
        )

    @property
    def router(self):
        return self.__router

    def book_trip(self, input_trip: InputTrip) -> OutputTrip:
        return self.__trip_booking_use_cases.book_trip(input_trip)

    def add_rental_car_reservation(
        self,
        trip_id: str,
        input_rental_car_reservation: InputRentalCarReservation,
    ) -> OutputRentalCarReservation:
        return self.__trip_booking_use_cases.add_rental_car_reservation(
            trip_id, input_rental_car_reservation
        )
