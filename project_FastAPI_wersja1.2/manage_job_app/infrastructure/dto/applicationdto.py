from datetime import datetime
from typing import Optional, Literal

from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from manage_job_app.infrastructure.dto.offerdto import OfferDTO
from manage_job_app.infrastructure.dto.userdto import UserDTO


class ApplicationDTO(BaseModel):
    """A model representing DTO for application data."""
    id: int
    offer_id: OfferDTO
    user_id: UserDTO
    cover_letter: Optional[str] = None
    status: Literal["sent", "under_review", "accepted", "rejected"] = "sent"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ApplicationDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ApplicationDTO: The final DTO instance.
        """
        record_dict = dict(record)
        print(record_dict)

        return cls(
            id=record_dict.get("id"),
            offer_id=OfferDTO(
                id=record_dict.get("id_1"),
                title=record_dict.get("title"),
                description=record_dict.get("description"),
                salary=record_dict.get("salary"),
                location=record_dict.get("location"),
                author_id=UserDTO(
                    id=record_dict.get("id_2"),
                    name=record_dict.get("name"),
                    email=record_dict.get("email"),
                    number=record_dict.get("number"),
                    city=record_dict.get("city"),
                    created_at=record_dict.get("created_at_2"),
                    updated_at=record_dict.get("updated_at_2"),
                ),
                created_at=record_dict.get("created_at_1"),
                updated_at=record_dict.get("updated_at_1")
            ),
            user_id=UserDTO(
                id=record_dict.get("id_3"),
                name=record_dict.get("name_1"),
                email=record_dict.get("email_1"),
                number=record_dict.get("number_1"),
                city=record_dict.get("city_1"),
                created_at=record_dict.get("created_at_3"),
                updated_at=record_dict.get("updated_at_3"),
            ),
            cover_letter=record_dict.get("cover_letter"),
            status=record_dict.get("status"),
            created_at=record_dict.get("created_at"),
            updated_at=record_dict.get("updated_at"),
        )

