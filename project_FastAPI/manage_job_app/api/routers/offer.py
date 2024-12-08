"""A module containing offer endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from manage_job_app.container import Container
from manage_job_app.core.domain.offer import Offer, OfferIn
from manage_job_app.infrastructure.dto.offerdto import OfferDTO
from manage_job_app.infrastructure.services.ioffer import IOfferService


router = APIRouter()



@router.post("/create", response_model=Offer, status_code=201)
@inject
async def create_offer(
    offer: OfferIn,
    service: IOfferService = Depends(Provide[Container.offer_service]),
) -> dict:
    """An endpoint for adding new offer.

       Args:
           offer (OfferIn): The offer data.
           service (IOfferService, optional): The injected service dependency.

       Returns:
           dict: The new offer attributes.
       """

    new_offer = await service.add_offer(offer)

    return new_offer.model_dump() if new_offer else {}


@router.get("/all", response_model=Iterable[OfferDTO], status_code=200)
@inject
async def get_all_offers(
    service: IOfferService = Depends(Provide[Container.offer_service]),
) -> Iterable:
    """An endpoint for getting all offers.

    Args:
        service (IOfferService, optional): The injected service dependency.

    Returns:
        Iterable: The offer attributes collection.
    """

    offers = await service.get_all()

    return offers


@router.get(
        "/{offer_id}",
        response_model=OfferDTO,
        status_code=200,
)
@inject
async def get_offer_by_id(
    offer_id: int,
    service: IOfferService = Depends(Provide[Container.offer_service]),
) -> dict | None:
    """An endpoint for getting offer by id.

    Args:
        offer_id (int): The id of the offer.
        service (IOfferService, optional): The injected service dependency.

    Returns:
        dict | None: The offer details.
    """

    if offer := await service.get_by_id(offer_id):
        return offer.model_dump()

    raise HTTPException(status_code=404, detail="Offer not found")


@router.get(
        "/user/{user_id}",
        response_model=Iterable[Offer],
        status_code=200,
)
@inject
async def get_offer_by_user(
    user_id: int,
    service: IOfferService = Depends(Provide[Container.offer_service]),
) -> Iterable:
    """An endpoint for getting offers by user who added them.

    Args:
        user_id (int): The id of the user.
        service (IOfferService, optional): The injected service dependency.

    Returns:
        Iterable: The offer details collection.
    """

    offers = await service.get_by_user(user_id)

    return offers


@router.put("/{offer_id}", response_model=Offer, status_code=201)
@inject
async def update_offer(
    offer_id: int,
    updated_offer: OfferIn,
    service: IOfferService = Depends(Provide[Container.offer_service]),
) -> dict:
    """An endpoint for updating offer data.

    Args:
        offer_id (int): The id of the offer.
        updated_offer (OfferIn): The updated offer details.
        service (IOfferService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if offer does not exist.

    Returns:
        dict: The updated offer details.
    """

    if await service.get_by_id(offer_id=offer_id):
        await service.update_offer(
            offer_id=offer_id,
            data=updated_offer,
        )
        return {**updated_offer.model_dump(), "id": offer_id}

    raise HTTPException(status_code=404, detail="Offer not found")


@router.delete("/{offer_id}", status_code=204)
@inject
async def delete_offer(
    offer_id: int,
    service: IOfferService = Depends(Provide[Container.offer_service]),
) -> None:
    """An endpoint for deleting offers.

    Args:
        offer_id (int): The id of the offer.
        service (IOfferService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if offer does not exist.
    """

    if await service.get_by_id(offer_id=offer_id):
        await service.delete_offer(offer_id)

        return

    raise HTTPException(status_code=404, detail="Offer not found")