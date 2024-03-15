from dependency_injector import containers, providers

from repositories.MongoDbTripRepository import MongoDbTripRepository
from services.reservation.flight.GalileoFlightReservationService import (
    GalileoFlightReservationService,
)
from services.reservation.hotel.AmadeusHotelReservationService import (
    AmadeusHotelReservationService,
)
from services.reservation.rentalcar.HertzRentalCarReservationService import (
    HertzRentalCarReservationService,
)
from usecases.TripBookingUsesCasesImpl import TripBookingUseCasesImpl


class DiContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            # ...
        ]
    )

    trip_booking_use_cases = providers.Singleton(TripBookingUseCasesImpl)
    trip_repository = providers.Singleton(MongoDbTripRepository)

    flight_reservation_service = providers.Singleton(
        GalileoFlightReservationService
    )

    hotel_reservation_service = providers.Singleton(
        AmadeusHotelReservationService
    )

    rental_car_reservation_service = providers.Singleton(
        HertzRentalCarReservationService
    )
