from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OfferIn(BaseModel):
    """Model representing offer's DTO attributes."""
    title: str
    description: str
    salary: int
    location: str
    author_id: int


class Offer(OfferIn):
    """Model representing offer's attributes in the database."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")