"""A module containing DTO models for output offers."""

from datetime import datetime
from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

from manage_job_app.core.domain.user import User
from manage_job_app.infrastructure.dto.userdto import UserDTO


class OfferDTO(BaseModel):
    """A model representing DTO for offer data."""
    id: int
    title: str
    description: str
    job_title: str
    salary: int
    location: str
    author_id: UserDTO
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "OfferDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            OfferDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            title=record_dict.get("title"),
            description=record_dict.get("description"),
            job_title=record_dict.get("job_title"),
            salary=record_dict.get("salary"),
            location=record_dict.get("location"),

            author_id=UserDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name"),
                email=record_dict.get("email"),
                number=record_dict.get("number"),
                city=record_dict.get("city"),
                created_at=record_dict.get("created_at_1"),
                updated_at=record_dict.get("updated_at_1"),
            ),
            created_at=record_dict.get("created_at"),
            updated_at=record_dict.get("updated_at"),
        )