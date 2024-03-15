from dependency_injector.wiring import Provide

from model.dtos.InputRentalCarReservation import InputRentalCarReservation
from model.dtos.InputTrip import InputTrip
from model.dtos.OutputRentalCarReservation import OutputRentalCarReservation
from model.dtos.OutputTrip import OutputTrip
from model.entities.RentalCarReservation import RentalCarReservation
from model.entities.Trip import Trip
from model.errors.EntityNotFoundError import EntityNotFoundError
from model.repositories.TripRepository import TripRepository
from model.usecases.TripBookingUseCases import TripBookingUseCases


class TripBookingUseCasesImpl(TripBookingUseCases):
    __trip_repository: TripRepository = Provide['trip_repository']

    def book_trip(self, input_trip: InputTrip) -> OutputTrip:
        # Below factory method creates a validated domain entity
        trip = Trip.create_from(input_trip)

        # Distributed transaction starts
        trip.make_reservations()

        try:
            self.__trip_repository.save(trip)
        except self.__trip_repository.Error as error:
            # Compensating action
            trip.cancel_reservations()
            raise error

        # Distributed transaction ends

        return OutputTrip.model_validate(trip)

    def add_rental_car_reservation(
        self,
        trip_id: str,
        input_rental_car_reservation: InputRentalCarReservation,
    ) -> OutputRentalCarReservation:
        # Get existing trip domain entity
        trip = self.__trip_repository.find(trip_id)

        if trip is None:
            raise EntityNotFoundError('Trip', trip_id)

        # Below factory method creates a validated domain entity
        rental_car_reservation = RentalCarReservation.create_from(
            input_rental_car_reservation
        )

        # Distributed transaction begins
        trip.add(rental_car_reservation)

        try:
            self.__trip_repository.update(trip)
        except self.__trip_repository.Error as error:
            # Compensating action
            trip.remove(rental_car_reservation)
            raise error

        # Distributed transaction ends

        return OutputRentalCarReservation.model_validate(
            rental_car_reservation
        )
