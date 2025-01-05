"""A model containing user-related models."""

from datetime import datetime
from typing import Optional, List, Literal

from pydantic import BaseModel, ConfigDict, UUID1, UUID4

from manage_job_app.core.domain.review import Review


class UserIn(BaseModel):
    """Model representing user's DTO attributes."""
    name: str
    email: str
    password: str
    number: Optional[str] = None
    city: Optional[str] = None

class EmployerIn(UserIn):
    company_name: Optional[str] = None

class Employer(EmployerIn):
    id: UUID4
    # role: Literal["employer"] = "employer"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class EmployeeIn(UserIn):
    skills: Optional[List[str]] = None

class Employee(EmployeeIn):
    id: UUID4
    # role: Literal["employee"] = "employee"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")


# class User(UserIn):
#     """Model representing user's attributes in the database."""
#     id: UUID4
#     created_at: datetime
#     updated_at: datetime
#
#     model_config = ConfigDict(from_attributes=True, extra="ignore")