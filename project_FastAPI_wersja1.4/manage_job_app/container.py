"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from manage_job_app.infrastructure.repositories.offerdb import \
    OfferRepository
from manage_job_app.infrastructure.repositories.userdb import \
    UserRepository
from manage_job_app.infrastructure.repositories.applicationdb import \
    ApplicationRepository
from manage_job_app.infrastructure.repositories.reviewdb import \
    ReviewRepository

from manage_job_app.infrastructure.services.offer import OfferService
from manage_job_app.infrastructure.services.user import UserService
from manage_job_app.infrastructure.services.application import ApplicationService
from manage_job_app.infrastructure.services.review import ReviewService

# from airportapi.infrastructure.repositories.airportmock import \
#     AirportMockRepository
# from airportapi.infrastructure.repositories.continentmock import \
#     ContinentRepository
# from airportapi.infrastructure.repositories.countrymock import \
#     CountryMockRepository
# from airportapi.infrastructure.services.airport import AirportService
# from airportapi.infrastructure.services.continent import ContinentService
# from airportapi.infrastructure.services.country import CountryService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    offer_repository = Singleton(OfferRepository)
    user_repository = Singleton(UserRepository)
    application_repository = Singleton(ApplicationRepository)
    review_repository = Singleton(ReviewRepository)

    # continent_repository = Singleton(ContinentRepository)
    # country_repository = Singleton(CountryMockRepository)
    # airport_repository = Singleton(AirportMockRepository)

    offer_service = Factory(
        OfferService,
        repository=offer_repository,
    )
    user_service = Factory(
        UserService,
        repository=user_repository,
    )
    application_service = Factory(
        ApplicationService,
        repository=application_repository,
    )
    review_service = Factory(
        ReviewService,
        repository=review_repository,
    )
    # continent_service = Factory(
    #     ContinentService,
    #     repository=continent_repository,
    # )
    # country_service = Factory(
    #     CountryService,
    #     repository=country_repository,
    # )
    # airport_service = Factory(
    #     AirportService,
    #     repository=airport_repository,
    # )

