from typing import List, Optional
from pydantic import BaseModel

# Historial_Medico.py
# Muestra todo lo que se le ha hecho al paciente.


class HistorialMedico(BaseModel):
    paciente: str
    registros: List[str]

    def mostrar_historial(self) -> None:
        print(f"Historial de {self.paciente}:")
        for r in self.registros:
            print(r)
