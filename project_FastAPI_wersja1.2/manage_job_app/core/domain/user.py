"""A model containing user-related models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID1, UUID4


class UserIn(BaseModel):
    """Model representing user's DTO attributes."""
    name: str
    email: str
    password: str
    number: Optional[str] = None
    city: Optional[str] = None


class User(UserIn):
    """Model representing user's attributes in the database."""
    id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")