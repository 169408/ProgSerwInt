"""A module containing DTO models for output reviews."""

from datetime import datetime
from typing import Optional, Literal
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, conint

from manage_job_app.core.domain.user import Employer, Employee
from manage_job_app.infrastructure.dto.userdto import EmployerDTO, EmployeeDTO


class ReviewDTO(BaseModel):
    """A model representing DTO for review data."""
    id: int
    employee_id: EmployeeDTO
    employer_id: EmployerDTO
    rating: conint(ge=1, le=10)
    review_text: str
    comments: Optional[str] = None
    status: Literal["visible", "hidden"] = "visible"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ReviewDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ReviewDTO: The final DTO instance.
        """
        record_dict = dict(record)
        print(record_dict)

        return cls(
            id=record_dict.get("id"),
            employee_id=EmployeeDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name"),
                email=record_dict.get("email"),
                number=record_dict.get("number"),
                city=record_dict.get("city"),
                skills=record_dict.get("skills"),
                created_at=record_dict.get("created_at_1"),
                updated_at=record_dict.get("updated_at_1"),
            ),
            employer_id=EmployerDTO(
                id=record_dict.get("id_2"),
                name=record_dict.get("name_1"),
                email=record_dict.get("email_1"),
                number=record_dict.get("number_1"),
                city=record_dict.get("city_1"),
                company_name=record_dict.get("company_get"),
                created_at=record_dict.get("created_at_2"),
                updated_at=record_dict.get("updated_at_2"),
            ),
            rating=record_dict.get("rating"),
            review_text=record_dict.get("review_text"),
            comments=record_dict.get("comments"),
            status=record_dict.get("status"),
            created_at=record_dict.get("created_at"),
            updated_at=record_dict.get("updated_at"),
        )