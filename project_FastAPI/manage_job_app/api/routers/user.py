"""A module containing user endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from manage_job_app.container import Container
from manage_job_app.core.domain.user import User, UserIn
from manage_job_app.infrastructure.dto.userdto import UserDTO
from manage_job_app.infrastructure.services.iuser import IUserService


router = APIRouter()



@router.post("/create", response_model=User, status_code=201)
@inject
async def create_user(
    user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """An endpoint for adding new user.

       Args:
           user (UserIn): The user data.
           service (IUserService, optional): The injected service dependency.

       Returns:
           dict: The new offer attributes.
       """

    new_user = await service.add_user(user)

    return new_user.model_dump() if new_user else {}


@router.get("/all", response_model=Iterable[UserDTO], status_code=200)
@inject
async def get_all_users(
    service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable:
    """An endpoint for getting all users.

    Args:
        service (IUserService, optional): The injected service dependency.

    Returns:
        Iterable: The user attributes collection.
    """

    users = await service.get_all()

    return users


@router.get(
        "/{user_id}",
        response_model=UserDTO,
        status_code=200,
)
@inject
async def get_user_by_id(
    user_id: int,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict | None:
    """An endpoint for getting user by id.

    Args:
        user_id (int): The id of the user.
        service (IUserService, optional): The injected service dependency.

    Returns:
        dict | None: The user details.
    """

    if user := await service.get_by_id(user_id):
        return user.model_dump()

    raise HTTPException(status_code=404, detail="User not found")


@router.get(
        "/user/{user_name}",
        response_model=Iterable[User],
        status_code=200,
)
@inject
async def find_users_by_name(
    user_name: str,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable:
    """An endpoint for finding users by name.

    Args:
        user_name (str): The name to search for.
        service (IUserService, optional): The injected service dependency.

    Returns:
        Iterable[User]: Users matching the name.
    """

    if users := await service.find_users_by_name(user_name):
        return users

    raise HTTPException(status_code=404, detail="Users not found")


@router.put("/{user_id}", response_model=User, status_code=201)
@inject
async def update_user(
    user_id: int,
    updated_user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """An endpoint for updating user data.

    Args:
        user_id (int): The id of the user.
        updated_user (UserIn): The updated user details.
        service (IUserService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if user does not exist.

    Returns:
        dict: The updated user details.
    """

    # if await service.get_by_id(user_id=user_id):
    #     await service.update_user(
    #         user_id=user_id,
    #         data=updated_user,
    #     )
    #     return {**updated_user.model_dump(), "id": user_id}

    if await service.get_by_id(user_id=user_id):
        updated_data = await service.update_user(
            user_id=user_id,
            data=updated_user,
        )

        return {**updated_data.model_dump(), "id": user_id}

    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=204)
@inject
async def delete_user(
    user_id: int,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> None:
    """An endpoint for deleting users.

    Args:
        user_id (int): The id of the user.
        service (IUserService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if user does not exist.
    """

    if await service.get_by_id(user_id=user_id):
        await service.delete_user(user_id)

        return

    raise HTTPException(status_code=404, detail="User not found")