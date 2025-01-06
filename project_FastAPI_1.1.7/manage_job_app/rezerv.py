manage_job_app/infrastructure/repositories/userdb.py

async def add_employer(self, data: EmployerIn) -> Any | None:
    """The method adding new user as employer to the data storage.

    Args:
        data (UserIn): The details of the new user.

    Returns:
        Any | None: The newly added user.
    """
    data.password = hash_password(data.password)
    query = employer_table.insert().values(**data.model_dump())
    new_employer_id = await database.execute(query)
    new_employer = await self._get_by_id(new_employer_id)

    return Employer(**dict(new_employer)) if new_employer else None


async def add_employee(self, data: EmployeeIn) -> Any | None:
    """The method adding new user as employee to the data storage.

    Args:
         data (UserIn): The details of the new user.

    Returns:
           Any | None: The newly added user.
    """

    data.password = hash_password(data.password)
    query = employee_table.insert().values(**data.model_dump())
    new_employee_id = await database.execute(query)
    new_employee = await self._get_by_id(new_employee_id)

    return Employee(**dict(new_employee)) if new_employee else None


async def update_employer(self, user_id: UUID5, data: EmployerIn) -> Any | None:
     """Updates employer details."""
    query_custom = select(employer_table).where(employer_table.c.id == user_id)
    user_custom = await database.fetch_one(query_custom)

    if await self._get_by_id(user_id):
        update_data = {
            **data.model_dump(),
               "created_at": user_custom["created_at"],
               "updated_at": datetime.now()
           }

           query = (
            employer_table.update()
               .where(employer_table.c.id == user_id)
               .values(**update_data)
        )
           await database.execute(query)

          user = await self._get_by_id(user_id)

        return Employer(**dict(user)) if user else None

    return None

async def update_employee(self, user_id: UUID5, data: EmployeeIn) -> Any | None:
    """Updates employer details."""
    query_custom = select(employee_table).where(employee_table.c.id == user_id)
    user_custom = await database.fetch_one(query_custom)

    if await self._get_by_id(user_id):
        update_data = {
            **data.model_dump(),
            "created_at": user_custom["created_at"],
            "updated_at": datetime.now()
        }

        query = (
            employee_table.update()
            .where(employee_table.c.id == user_id)
            .values(**update_data)
        )
        await database.execute(query)

        user = await self._get_by_id(user_id)

        return Employee(**dict(user)) if user else None

    return None




async def delete_employer(self, user_id: UUID5) -> bool:
    """Deletes an employer by ID."""

    if await self._get_by_id(user_id):
        query = employer_table \
            .delete() \
            .where(employer_table.c.id == user_id)
        await database.execute(query)
        return True

    return False

async def delete_employee(self, user_id: UUID5) -> bool:
    """Deletes an employee by ID."""

    if await self._get_by_id(user_id):
        query = employee_table \
            .delete() \
            .where(employee_table.c.id == user_id)
        await database.execute(query)
        return True

    return False






--------------------------------------
--------------------------------------
--manage_job_app/api/routers/user.py--
--------------------------------------
--------------------------------------


"""A module containing user endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from pydantic import UUID4

from manage_job_app.infrastructure.utils import consts
from manage_job_app.container import Container
from manage_job_app.core.domain.user import Employer, Employee, EmployerIn, EmployeeIn, UserIn
from manage_job_app.infrastructure.dto.userdto import EmployerDTO, EmployeeDTO
from manage_job_app.infrastructure.services.iuser import IUserService
from manage_job_app.infrastructure.dto.tokendto import TokenDTO

bearer_scheme = HTTPBearer()

router = APIRouter()



@router.post("/register", response_model=User, status_code=201)
@inject
async def add_user(
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

    if new_user := await service.add_user(user):
        return new_user.model_dump() if new_user else {}

    raise HTTPException(
        status_code=400,
        detail="The user with provided e-mail already exists",
    )

@router.post("/token", response_model=TokenDTO, status_code=200)
@inject
async def authenticate_user(
    user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for authenticating users.

    Args:
        user (UserIn): The user input datapp.infrastructure.dto.tokendto import TokenDTO
.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The token DTO details.
    """

    if token_details := await service.authenticate_user(user):
        print("user confirmed")
        return token_details.model_dump()

    raise HTTPException(
        status_code=401,
        detail="Provided incorrect credentials",
    )

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
    user_id: UUID4,
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
        response_model=Iterable[UserDTO],
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
    user_id: UUID4,
    updated_user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating user data.

    Args:
        user_id (int): The id of the user.
        updated_user (UserIn): The updated user details.
        service (IUserService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

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

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if user_data := await service.get_by_id(user_id=user_id):
        if str(user_data.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        updated_data = await service.update_user(
            user_id=user_id,
            data=updated_user,
        )

        return {**updated_data.model_dump(), "id": user_id}

    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=204)
@inject
async def delete_user(
    user_id: UUID4,
    service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting users.

    Args:
        user_id (int): The id of the user.
        service (IUserService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if user does not exist.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if user_data := await service.get_by_id(user_id=user_id):
        if str(user_data.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        await service.delete_user(user_id)

        return

    raise HTTPException(status_code=404, detail="User not found")








