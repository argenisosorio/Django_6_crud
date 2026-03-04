from dataclasses import dataclass
from typing import Optional

"""
Este módulo define los objetos de transferencia de datos (DTO) para la
aplicación de personas. Los DTO se utilizan para encapsular los datos que se
envían entre las capas de la aplicación, permitiendo una separación clara entre
la lógica de negocio y la presentación.
"""


# Objeto de transferencia de datos (DTO) para crear una nueva persona
@dataclass(frozen=True)
class PersonDTO:
    name: str
    email: str
    age: int


# Objeto de transferencia de datos (DTO) para actualizar una persona existente
@dataclass(frozen=True)
class UpdatePersonDTO:
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
