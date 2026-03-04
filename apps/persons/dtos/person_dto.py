from dataclasses import dataclass
from typing import Optional


# Data Transfer Object (DTO) for creating a new Person
@dataclass(frozen=True)
class PersonDTO:
    name: str
    email: str
    age: int


# Data Transfer Object (DTO) for updating an existing Person
@dataclass(frozen=True)
class UpdatePersonDTO:
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
