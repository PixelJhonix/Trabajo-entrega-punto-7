from typing import List, Optional
from pydantic import BaseModel

# Profesional.py
# Aquí se registra el médico o enfermera con sus datos.


class Profesional(BaseModel):
    nombre: str
    categoria_profesional: str  # 'doctor' o 'enfermera'
