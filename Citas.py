from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# Citas.py
# Manejo de citas: agendar, ver por paciente/medico/fecha, cancelar.


class Citas(BaseModel):
    usuario: str
    profesional: str
    fecha: datetime

    @staticmethod
    def ver_citas_paciente(nombre: str, citas_list: List["Citas"]) -> None:
        print(f"Citas de {nombre}:")
        for c in citas_list:
            if c.usuario == nombre:
                print(f"Con {c.profesional} el {c.fecha}")

    @staticmethod
    def ver_citas_medico(nombre: str, citas_list: List["Citas"]) -> None:
        print(f"Citas de {nombre}:")
        for c in citas_list:
            if c.profesional == nombre:
                print(f"Con {c.usuario} el {c.fecha}")

    @staticmethod
    def ver_citas_fecha(fecha: str, citas_list: List["Citas"]) -> None:
        print(f"Citas en {fecha}:")
        for c in citas_list:
            if c.fecha == fecha:
                print(f"{c.usuario} con {c.profesional}")

    @staticmethod
    def cancelar_cita(
        usuario: str, profesional: str, fecha: datetime, citas_list: List["Citas"]
    ) -> None:
        for i, c in enumerate(citas_list):
            if (
                c.usuario == usuario
                and c.profesional == profesional
                and c.fecha == fecha
            ):
                del citas_list[i]
                print("Cita cancelada.")
                return
        print("Cita no encontrada.")
