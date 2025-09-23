from typing import List, Optional
from pydantic import BaseModel

# Usuario.py
# Registro de datos del usuario, diagnóstico y decisión de profesional needed.


class Usuario(BaseModel):
    nombre: str
    edad: int
    diagnostico: str
    necesita: str  # 'doctor' o 'enfermera'
