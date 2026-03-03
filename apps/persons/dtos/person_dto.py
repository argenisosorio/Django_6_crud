from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PersonDTO:
    name: str
    email: str
    age: int


@dataclass(frozen=True)
class UpdatePersonDTO:
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

