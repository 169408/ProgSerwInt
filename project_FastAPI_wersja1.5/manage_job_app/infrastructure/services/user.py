"""Module containing user service implementation."""

from typing import Iterable

from pydantic import UUID4

from manage_job_app.core.domain.user import User, UserIn
from manage_job_app.core.repositories.iuser import IUserRepository
from manage_job_app.infrastructure.dto.userdto import UserDTO
from manage_job_app.infrastructure.services.iuser import IUserService
from manage_job_app.infrastructure.dto.tokendto import TokenDTO
from manage_job_app.infrastructure.utils.password import verify_password
from manage_job_app.infrastructure.utils.token import generate_user_token

class UserService(IUserService):
    """A class implementing the user service."""

    _repository: IUserRepository

    def __init__(self, repository: IUserRepository) -> None:
        """The initializer of the `user service`.

        Args:
            repository (IUserRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[UserDTO]:
        """The method getting all users from the repository.

        Returns:
            Iterable[UserDTO]: All users.
        """

        return await self._repository.get_all_users()

    async def get_by_id(self, user_id: UUID4) -> UserDTO | None:
        """The method getting user by provided id.

        Args:
            user_id (UUID4): The id of the user.

        Returns:
            UserDTO | None: The offer details.
        """

        return await self._repository.get_by_id(user_id)

    async def get_by_email(self, email: str) -> UserDTO | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

        return await self.get_by_email(email)

    async def find_users_by_name(self, user_name: str) -> Iterable[UserDTO]:
        """The method to find users by name.

        Args:
            user_name (str): The name or part of the name to search for.

        Returns:
            Iterable[UserDTO]: A list of users matching the name criteria.
        """

        return await self._repository.find_users_by_name(user_name)

    async def add_user(self, data: UserIn) -> User | None:
        """The method adding new user to the data storage.

        Args:
            data (UserIn): The details of the new user.

        Returns:
            User | None: The newly added user.
        """

        return await self._repository.add_user(data)

    async def authenticate_user(self, data: UserIn) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            data (UserIn): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

        if user_data := await self._repository.get_by_email(data.email):
            if verify_password(data.password, user_data.password):
                token_details = generate_user_token(user_data.id)
                # trunk-ignore(bandit/B106)
                return TokenDTO(token_type="Bearer", **token_details)

            return None

        return None

    async def update_user(self, user_id: UUID4, data: UserIn) -> User | None:
        """The method updating user data in the data storage.

        Args:
            user_id (UUID4): The id of the user.
            data (UserIn): The details of the updated user.

        Returns:
            User | None: The updated user details.
        """

        return await self._repository.update_user(user_id=user_id, data=data)

    async def delete_user(self, user_id: UUID4) -> bool:
        """The method removing a user from the data storage.

        Args:
            user_id (UUID4): The id of the user.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_user(user_id)