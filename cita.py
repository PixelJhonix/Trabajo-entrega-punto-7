from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import List

class CitaIn(BaseModel):
    """Modelo de entrada para validar datos de cita"""
    fecha: str = Field(pattern=r"^\d{2}/\d{2}/\d{4}$")  # dd/mm/yyyy
    hora: str = Field(pattern=r"^\d{2}:\d{2}$")  # HH:MM
    motivo: str = Field(min_length=5, max_length=200)

    @field_validator("fecha")
    @classmethod
    def validar_fecha(cls, v: str) -> str:
        """Valida que la fecha sea futura y válida"""
        try:
            fecha_obj = datetime.strptime(v, "%d/%m/%Y")
            if fecha_obj < datetime.now():
                raise ValueError("La fecha debe ser futura")
            return v
        except ValueError as e:
            raise ValueError(f"Formato de fecha inválido o fecha pasada: {e}")

    @field_validator("hora")
    @classmethod
    def validar_hora(cls, v: str) -> str:
        """Valida que la hora esté en horario laboral"""
        try:
            hora, minuto = map(int, v.split(":"))
            if not (8 <= hora <= 18) or not (0 <= minuto <= 59):
                raise ValueError("Hora debe estar entre 8:00 y 18:00")
            return v
        except ValueError as e:
            raise ValueError(f"Hora inválida: {e}")

class Cita:
    """Clase para gestionar citas médicas"""
    
    def __init__(self, paciente, medico, fecha: str, hora: str, motivo: str):
        self.paciente = paciente
        self.medico = medico
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
        self.estado = "Agendada"
        self.fecha_creacion = datetime.now()
    
    def mostrar_cita(self):
        """Muestra los detalles de la cita"""
        print(f"--- CITA MÉDICA ---")
        print(f"Paciente: {self.paciente._nombre}")
        print(f"Médico: {self.medico._nombre}")
        print(f"Fecha: {self.fecha}")
        print(f"Hora: {self.hora}")
        print(f"Motivo: {self.motivo}")
        print(f"Estado: {self.estado}")
        print(f"Fecha de creación: {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}")

    @staticmethod
    def verificar_disponibilidad(medico, fecha: str, hora: str) -> bool:
        """Verifica si el médico está disponible en esa fecha y hora"""
        if not hasattr(medico, '_citas'):
            return True
        
        for cita in medico._citas:
            if cita.fecha == fecha and cita.hora == hora and cita.estado != "Cancelada":
                return False
        return True

    @staticmethod
    def verificar_disponibilidad_paciente(paciente, fecha: str, hora: str) -> bool:
        """Verifica si el paciente no tiene otra cita en esa fecha y hora"""
        if not hasattr(paciente, '_citas'):
            return True
        
        for cita in paciente._citas:
            if cita.fecha == fecha and cita.hora == hora and cita.estado != "Cancelada":
                return False
        return True
