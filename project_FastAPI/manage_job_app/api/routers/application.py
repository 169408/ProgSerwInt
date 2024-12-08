"""A module containing application endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from manage_job_app.container import Container
from manage_job_app.core.domain.application import Application, ApplicationIn
from manage_job_app.infrastructure.dto.applicationdto import ApplicationDTO
from manage_job_app.infrastructure.services.iapplication import IApplicationService


router = APIRouter()



@router.post("/create", response_model=Application, status_code=201)
@inject
async def create_application(
    application: ApplicationIn,
    service: IApplicationService = Depends(Provide[Container.application_service]),
) -> dict:
    """An endpoint for adding new application.

       Args:
           application (ApplicationIn): The application data.
           service (IApplicationService, optional): The injected service dependency.

       Returns:
           dict: The new application attributes.
       """

    new_application = await service.add_application(application)

    return new_application.model_dump() if new_application else {}


@router.get("/all", response_model=Iterable[ApplicationDTO], status_code=200)
@inject
async def get_all_applications(
    service: IApplicationService = Depends(Provide[Container.application_service]),
) -> Iterable:
    """An endpoint for getting all applications.

    Args:
        service (IApplicationService, optional): The injected service dependency.

    Returns:
        Iterable: The application attributes collection.
    """

    applications = await service.get_all()

    return applications


@router.get(
        "/{application_id}",
        response_model=ApplicationDTO,
        status_code=200,
)
@inject
async def get_application_by_id(
    application_id: int,
    service: IApplicationService = Depends(Provide[Container.application_service]),
) -> dict | None:
    """An endpoint for getting application by id.

    Args:
        application_id (int): The id of the application.
        service (IApplicationService, optional): The injected service dependency.

    Returns:
        dict | None: The application details.
    """

    if application := await service.get_by_id(application_id):
        return application.model_dump()

    raise HTTPException(status_code=404, detail="Application not found")


@router.get(
        "/user/{user_id}",
        response_model=Iterable[Application],
        status_code=200,
)
@inject
async def get_application_by_user(
    user_id: int,
    service: IApplicationService = Depends(Provide[Container.application_service]),
) -> Iterable:
    """An endpoint for getting applications by user who added them.

    Args:
        user_id (int): The id of the user.
        service (IApplicationService, optional): The injected service dependency.

    Returns:
        Iterable: The application details collection.
    """

    applications = await service.get_by_user(user_id)

    return applications


@router.put("/{application_id}", response_model=Application, status_code=201)
@inject
async def update_offer(
    application_id: int,
    updated_application: ApplicationIn,
    service: IApplicationService = Depends(Provide[Container.application_service]),
) -> dict:
    """An endpoint for updating application data.

    Args:
        application_id (int): The id of the application.
        updated_application (ApplicationIn): The updated application details.
        service (IApplicationService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if application does not exist.

    Returns:
        dict: The updated application details.
    """

    if await service.get_by_id(application_id=application_id):
        await service.update_application(
            application_id=application_id,
            data=updated_application,
        )
        return {**updated_application.model_dump(), "id": application_id}

    raise HTTPException(status_code=404, detail="Application not found")


@router.delete("/{application_id}", status_code=204)
@inject
async def delete_application(
    application_id: int,
    service: IApplicationService = Depends(Provide[Container.application_service]),
) -> None:
    """An endpoint for deleting applications.

    Args:
        application_id (int): The id of the application.
        service (IApplicationService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if application does not exist.
    """

    if await service.get_by_id(application_id=application_id):
        await service.delete_application(application_id)

        return

    raise HTTPException(status_code=404, detail="Application not found")