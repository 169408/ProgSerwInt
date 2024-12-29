"""A module containing DTO models for output users."""
from datetime import datetime
from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4



class UserDTO(BaseModel):
    """A model representing DTO for user data."""
    id: UUID4
    name: str
    email: str
    number: Optional[str] = None
    city: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore", arbitrary_types_allowed=True,)

    @classmethod
    def from_record(cls, record: Record) -> "UserDTO":
        """A method to create a UserDTO instance from a DB record."""

        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            email=record_dict.get("email"),
            number=record_dict.get("number"),
            city=record_dict.get("city"),
            created_at=record_dict.get("created_at"),
            updated_at=record_dict.get("updated_at")
        )
