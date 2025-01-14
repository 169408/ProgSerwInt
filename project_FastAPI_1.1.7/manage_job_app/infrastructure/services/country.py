"""Module containing country service implementation."""

from typing import Iterable


from manage_job_app.core.domain.location import Country, CountryIn
from manage_job_app.core.repositories.icountry import ICountryRepository
from manage_job_app.infrastructure.services.icountry import ICountryService


class CountryService(ICountryService):
    """A class implementing the country service."""

    _repository: ICountryRepository

    def __init__(self, repository: ICountryRepository) -> None:
        """The initializer of the `country service`.

        Args:
            repository (ICountryRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all_countries(self) -> Iterable[Country]:
        """The method getting all countries from the repository.

        Returns:
            Iterable[country]: The collection of the all countries.
        """

        return await self._repository.get_all_countries()

    async def get_country_by_id(self, country_id: int) -> Country | None:
        """The method getting a country from the repository.

        Args:
            country_id (int): The id of the country.

        Returns:
            country | None: The country data if exists.
        """

        return await self._repository.get_country_by_id(country_id)

    async def get_countries_by_continent(
            self,
            continent_id: int,
    ) -> Iterable[Country]:
        """The abstract getting all provided continent's countries
            from the repository.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Iterable[Country]: The collection of the countries.
        """

        return await self._repository.get_countries_by_continent(continent_id)


    async def add_country(self, data: CountryIn) -> Country | None:
        """The method adding new country to the repository.

        Args:
            data (CountryIn): The attributes of the country.

        Returns:
            Country | None: The newly created country.
        """

        return await self._repository.add_country(data)

    async def update_country(
        self,
        country_id: int,
        data: CountryIn,
    ) -> Country | None:
        """The method updating country data in the repository.

        Args:
            country_id (int): The country id.
            data (CountryIn): The attributes of the country.

        Returns:
            Country | None: The updated country.
        """

        return await self._repository.update_country(
            country_id=country_id,
            data=data,
        )

    async def delete_country(self, country_id: int) -> bool:
        """The method updating removing country from the repository.

        Args:
            country_id (int): The country id.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_country(country_id)