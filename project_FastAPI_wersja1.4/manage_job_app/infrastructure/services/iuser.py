"""Module containing user service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID5

from manage_job_app.core.domain.user import User, UserIn
from manage_job_app.infrastructure.dto.tokendto import TokenDTO
from manage_job_app.infrastructure.dto.userdto import UserDTO


class IUserService(ABC):
    """A class representing user repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[UserDTO]:
        """The method getting all users from the repository.

        Returns:
            Iterable[UserDTO]: All users.
        """

    @abstractmethod
    async def get_by_id(self, user_id: UUID5) -> UserDTO | None:
        """The method getting user by provided id.

        Args:
            user_id (UUID5): The ID of the user.

        Returns:
            UserDTO | None: The user details.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDTO | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

    @abstractmethod
    async def find_users_by_name(self, user_name: str) -> Iterable[UserDTO]:
        """The method to find users by name.

        Args:
            user_name (str): The name or part of the name to search for.

        Returns:
            Iterable[UserDTO]: A list of users matching the name criteria.
        """

    @abstractmethod
    async def add_user(self, data: UserIn) -> User | None:
        """The method adding new user to the data storage.

        Args:
            data (UserIn): The data of the new user.

        Returns:
            User | None: Full details of the newly added user.
        """

    @abstractmethod
    async def authenticate_user(self, data: UserIn) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            data (UserIn): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

    @abstractmethod
    async def update_user(self, user_id: UUID5, data: UserIn) -> User | None:
        """The method updating user data in the data storage.

        Args:
            user_id (UUID5): The ID of the user.
            data (OfferIn): The new data for the user.

        Returns:
            User | None: The updated user details.
        """

    @abstractmethod
    async def delete_user(self, user_id: UUID5) -> bool:
        """The method updating removing user from the data storage.

        Args:
            user_id (UUID5): The ID of the user.

        Returns:
            bool: Success of the operation.
        """