from typing import List, Optional
from pydantic import BaseModel

# Factura.py
# Genera factura con lo que necesitaba el paciente y descripción.


class Factura(BaseModel):
    usuario: str
    descripcion: str
    monto: float

    def mostrar_factura(self) -> None:
        print(f"Factura para {self.usuario}: {self.descripcion} - Monto: {self.monto}")
