from dependency_injector import containers, providers

from ifadapters.repositories.MongoDbTripRepository import MongoDbTripRepository
from ifadapters.services.reservation.AmadeusHotelReservationService import (
    AmadeusHotelReservationService,
)
from ifadapters.services.reservation.GalileoFlightReservationService import (
    GalileoFlightReservationService,
)
from ifadapters.services.reservation.HertzRentalCarReservationService import (
    HertzRentalCarReservationService,
)
from model.usecases.TripBookingUsesCasesImpl import TripBookingUseCasesImpl


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
