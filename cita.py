from datetime import datetime
from typing import List, Optional
from schemas import CitaIn

class Cita:
    """
    Clase para gestionar citas médicas en el sistema hospitalario.
    
    Esta clase encapsula toda la información relacionada con
    una cita médica entre un paciente y un médico.
    
    Attributes:
        paciente: Paciente que solicita la cita
        medico: Médico que atenderá la cita
        fecha: Fecha de la cita en formato dd/mm/yyyy
        hora: Hora de la cita en formato HH:MM
        motivo: Motivo de la consulta
        estado: Estado actual de la cita (Agendada, Cancelada, Completada)
        fecha_creacion: Fecha y hora de creación del registro
    """
    
    def __init__(self, paciente, medico, fecha: str, hora: str, motivo: str) -> None:
        """
        Inicializa una nueva instancia de Cita.
        
        Args:
            paciente: Paciente que solicita la cita
            medico: Médico que atenderá la cita
            fecha: Fecha de la cita en formato dd/mm/yyyy
            hora: Hora de la cita en formato HH:MM
            motivo: Motivo de la consulta
        """
        self.paciente = paciente
        self.medico = medico
        self.fecha: str = fecha
        self.hora: str = hora
        self.motivo: str = motivo
        self.estado: str = "Agendada"
        self.fecha_creacion: datetime = datetime.now()
    
    def mostrar_cita(self) -> None:
        """
        Muestra los detalles de la cita.
        
        Este método imprime en consola toda la información
        relacionada con la cita de forma legible.
        """
        print(f"--- CITA MÉDICA ---")
        print(f"Paciente: {self.paciente._nombre}")
        print(f"Médico: {self.medico._nombre}")
        print(f"Fecha: {self.fecha}")
        print(f"Hora: {self.hora}")
        print(f"Motivo: {self.motivo}")
        print(f"Estado: {self.estado}")
        print(f"Fecha de creación: {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}")

    def cancelar(self) -> None:
        """
        Cancela la cita médica.
        
        Este método cambia el estado de la cita a "Cancelada".
        """
        self.estado = "Cancelada"
        print(f"Cita cancelada para {self.fecha} a las {self.hora}")

    def completar(self) -> None:
        """
        Marca la cita como completada.
        
        Este método cambia el estado de la cita a "Completada".
        """
        self.estado = "Completada"
        print(f"Cita completada para {self.fecha} a las {self.hora}")

    @staticmethod
    def verificar_disponibilidad(medico, fecha: str, hora: str) -> bool:
        """
        Verifica si el médico está disponible en esa fecha y hora.
        
        Args:
            medico: Médico a verificar disponibilidad
            fecha: Fecha a verificar
            hora: Hora a verificar
            
        Returns:
            bool: True si el médico está disponible, False en caso contrario
        """
        if not hasattr(medico, '_citas'):
            return True
        
        for cita in medico._citas:
            if cita.fecha == fecha and cita.hora == hora and cita.estado != "Cancelada":
                return False
        return True

    @staticmethod
    def verificar_disponibilidad_paciente(paciente, fecha: str, hora: str) -> bool:
        """
        Verifica si el paciente no tiene otra cita en esa fecha y hora.
        
        Args:
            paciente: Paciente a verificar disponibilidad
            fecha: Fecha a verificar
            hora: Hora a verificar
            
        Returns:
            bool: True si el paciente está disponible, False en caso contrario
        """
        if not hasattr(paciente, '_citas'):
            return True
        
        for cita in paciente._citas:
            if cita.fecha == fecha and cita.hora == hora and cita.estado != "Cancelada":
                return False
        return True

    def __str__(self) -> str:
        """
        Retorna una representación en string de la cita.
        
        Returns:
            str: Representación de la cita
        """
        return f"Cita: {self.paciente._nombre} con Dr. {self.medico._nombre} el {self.fecha} a las {self.hora}"

    def __repr__(self) -> str:
        """
        Retorna una representación técnica de la cita.
        
        Returns:
            str: Representación técnica de la cita
        """
        return f"Cita(paciente='{self.paciente._nombre}', medico='{self.medico._nombre}', fecha='{self.fecha}', hora='{self.hora}')"
