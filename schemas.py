from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class Turno(str, Enum):
    manana = "Mañana"
    tarde = "Tarde"
    noche = "Noche"

class PersonaIn(BaseModel):
    nombre: str = Field(min_length=1)
    fecha_nac: str  # Formato dd/mm/yyyy
    telefono: str = Field(pattern=r"^[0-9+\-\s]{7,15}$")
    direccion: str = Field(min_length=3)

    @field_validator("fecha_nac")
    @classmethod
    def validar_fecha(cls, v: str) -> str:
        datetime.strptime(v, "%d/%m/%Y")
        return v

class PacienteIn(PersonaIn):
    pass

class MedicoIn(PersonaIn):
    especialidad: str = Field(min_length=2)

class EnfermeraIn(PersonaIn):
    turno: Turno
