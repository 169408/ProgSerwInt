from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict


class ApplicationIn(BaseModel):
    """Model representing application's DTO attributes."""
    offer_id: int
    user_id: int
    cover_letter: Optional[str] = None
    status: Literal["sent", "under_review", "accepted", "rejected"] = "sent"


class Application(ApplicationIn):
    """Model representing application's attributes in the database."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")