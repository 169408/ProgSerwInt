"""Module containing user repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from manage_job_app.core.domain.user import UserIn


class IUserRepository(ABC):
    """An abstract class representing protocol of user repository."""

    @abstractmethod
    async def get_all_users(self) -> Iterable[Any]:
        """The abstract getting all users from the data storage.

        Returns:
            Iterable[User]: Users in the data storage.
        """


    @abstractmethod
    async def get_by_id(self, user_id: int) -> Any | None:
        """The abstract getting user by provided id.

        Args:
            user_id (int): The id of the user.

        Returns:
            User | None: The user details.
        """

    @abstractmethod
    async def find_users_by_name(self, user_name: str) -> Iterable[Any]:
        """The abstract finding users by name.

        Args:
            user_name (str): The name to search for.

        Returns:
            Iterable[User]: Users matching the name.
        """


    @abstractmethod
    async def add_user(self, data: UserIn) -> Any | None:
        """The abstract adding new user to the data storage.

        Args:
            data (UserIn): The details of the new user.

        Returns:
            Any | None: The newly added user.
        """

    @abstractmethod
    async def update_user(
        self,
        user_id: int,
        data: UserIn,
    ) -> Any | None:
        """The abstract updating user data in the data storage.

        Args:
            user_id (int): The id of the user.
            data (UserIn): The details of the updated user.

        Returns:
            User | None: The updated user details.
        """

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        """The abstract updating removing user from the data storage.

        Args:
            user_id (int): The id of the user.

        Returns:
            bool: Success of the operation.
        """
