from pydantic import BaseModel, ConfigDict


class ContinentIn(BaseModel):
    """Model representing continent's DTO attributes."""
    name: str
    alias: str


class Continent(ContinentIn):
    """Model representing continent's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class CountryIn(BaseModel):
    """Model representing country's DTO attributes."""
    name: str
    alias: str
    continent_id: int


class Country(CountryIn):
    """Model representing continent's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class CityIn(BaseModel):
    """Model representing city's DTO attributes."""
    name: str
    country_id: int

class City(CityIn):
    """Model representing city's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
