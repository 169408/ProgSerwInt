from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, UUID4


class ApplicationIn(BaseModel):
    """Model representing application's DTO attributes."""
    offer_id: int
    cover_letter: Optional[str] = None

class ApplicationBroker(ApplicationIn):
    user_id: UUID4
    status: Literal["sent", "under_review", "accepted", "rejected"] = "sent"

class Application(ApplicationBroker):
    """Model representing application's attributes in the database."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")