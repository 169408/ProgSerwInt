"""Module containing offer repository implementation."""

from typing import Iterable

from manage_job_app.core.repositories.ioffer import IOfferRepository
from manage_job_app.core.domain.offer import Offer, OfferIn
from manage_job_app.infrastructure.repositories.db import offers


class OfferMockRepository(IOfferRepository):
    """A class representing continent repository."""

    async def get_all_offers(self) -> Iterable[Offer]:
        """The method getting all offers from the data storage.

        Returns:
            Iterable[Offer]: Offers in the data storage.
        """

        return offers


    async def get_by_id(self, offer_id: int) -> Offer | None:
        """The method getting offer by provided id.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            Offer | None: The offer details.
        """

        return next((obj for obj in offers if obj.id == offer_id), None)


    async def get_by_user(self, user_id: int) -> Iterable[Offer]:
        """The method getting offers by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Offer]: The offer collection.
        """

        return list(filter(lambda x: x.user_id == user_id, offers))

    async def search_by_title(self, title: str) -> Iterable[Offer]:
        """The method getting searched offers by title.

            Args:
            title (str): The title of the offer.

        Returns:
            Iterable[Offer]: A collection of offers matching the title.
        """
        return list(filter(lambda x: title.lower() in x.title.lower(), offers))


    async def add_offer(self, data: OfferIn) -> None:
        """The method adding new offer to the data storage.

        Args:
            data (OfferIn): The details of the new offer.

        Returns:
            Offer: Full details of the newly added offer.
        """

        offers.append(data)

    async def update_offer(
        self,
        offer_id: int,
        data: OfferIn,
    ) -> Offer | None:
        """The method updating offer data in the data storage.

        Args:
            offer_id (int): The id of the offer.
            data (OfferIn): The details of the updated offer.

        Returns:
            Offer | None: The updated offer details.
        """

        if offer_pos := \
                next(filter(lambda x: x.id == offer_id, offers)):
            offers[offer_pos] = data

            return Offer(id=0, **data.model_dump())

        return None

    async def delete_offer(self, offer_id: int) -> bool:
        """The method updating removing offer from the data storage.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            bool: Success of the operation.
        """

        if offer_pos := \
                next(filter(lambda x: x.id == offer_id, offers)):
            offers.remove(offer_pos)
            return True

        return False