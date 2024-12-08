"""Module containing user repository implementation."""
from datetime import datetime
from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join, func

from manage_job_app.core.repositories.iuser import IUserRepository
from manage_job_app.core.domain.user import User, UserIn
from manage_job_app.db import (
    user_table,
    database,
)
from manage_job_app.infrastructure.dto.userdto import UserDTO


class UserRepository(IUserRepository):
    """A class representing user DB repository."""

    async def get_all_users(self) -> Iterable[Any]:
        """The method getting all users from the data storage.

        Returns:
            Iterable[Any]: Users in the data storage.
        """

        columns_to_select = [
            column for column in user_table.c if column.name != "password"
        ]
        query = (
            select(*columns_to_select)
            .order_by(user_table.c.name.asc())
        )

        users = await database.fetch_all(query)

        return [UserDTO.from_record(user) for user in users]


    async def get_by_id(self, user_id: int) -> Any | None:
        """The method getting user by provided id.

        Args:
            user_id (int): The id of the user.

        Returns:
            Any | None: The user details.
        """

        query = select(user_table).where(user_table.c.id == user_id)
        user = await database.fetch_one(query)

        return UserDTO.from_record(user) if user else None

    async def find_users_by_name(self, user_name: str) -> Iterable[Any]:
        """The method to find users by name.

        Args:
            user_name (str): The name or part of the name to search for.

        Returns:
            Iterable[Any]: A list of users matching the name criteria.
        """
        query = (
            select(user_table)
            .where(func.lower(user_table.c.name).like(f"%{user_name.lower()}%"))
            .order_by(user_table.c.name.asc())
        )

        users = await database.fetch_all(query)
        return [UserDTO.from_record(user) for user in users]

    async def add_user(self, data: UserIn) -> Any | None:
        """The method adding new user to the data storage.

        Args:
            data (UserIn): The details of the new user.

        Returns:
            Any | None: The newly added user.
        """

        query = user_table.insert().values(**data.model_dump())
        new_user_id = await database.execute(query)
        new_user = await self._get_by_id(new_user_id)

        return User(**dict(new_user)) if new_user else None

    async def update_user(self, user_id: int, data: UserIn) -> Any | None:
        """The method updating user data in the data storage.

        Args:
            user_id (int): The id of the user.
            data (UserIn): The details of the updated user.

        Returns:
            Any | None: The updated user details.
        """
        query_custom = select(user_table).where(user_table.c.id == user_id)
        user_custom = await database.fetch_one(query_custom)

        if await self._get_by_id(user_id):
            update_data = {
                **data.model_dump(),
                "created_at": user_custom["created_at"],
                "updated_at": datetime.now()
            }

            query = (
                user_table.update()
                .where(user_table.c.id == user_id)
                .values(**update_data)
            )
            await database.execute(query)

            user = await self._get_by_id(user_id)

            return User(**dict(user)) if user else None

        return None

    # async def update_user(self, user_id: int, data: UserIn) -> User | None:
    #     query_custom = select(user_table).where(user_table.c.id == user_id)
    #     user_custom = await database.fetch_one(query_custom)
    #
    #     if user_custom:
    #         update_data = {
    #             **data.model_dump(),
    #             "created_at": user_custom["created_at"],
    #             "updated_at": datetime.now()
    #         }
    #
    #         query = (
    #             user_table.update()
    #             .where(user_table.c.id == user_id)
    #             .values(**update_data)
    #         )
    #         await database.execute(query)
    #
    #         updated_user_query = select(user_table).where(user_table.c.id == user_id)
    #         updated_user = await database.fetch_one(updated_user_query)
    #         return User(**dict(updated_user)) if updated_user else None
    #
    #     return None

    async def delete_user(self, user_id: int) -> bool:
        """The method removing a user from the data storage.

        Args:
            user_id (int): The id of the user.

        Returns:
            bool: Success of the operation.
        """

        if await self._get_by_id(user_id):
            query = user_table \
                .delete() \
                .where(user_table.c.id == user_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, user_id: int) -> Record | None:
        """A private method getting user from the DB based on its ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Any | None: User record if exists.
        """

        query = (
            user_table.select()
            .where(user_table.c.id == user_id)
            .order_by(user_table.c.name.asc())
        )
        return await database.fetch_one(query)