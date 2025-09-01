"""
Clase para gestionar pacientes en el Sistema Hospitalario.

Este módulo contiene la clase Paciente que hereda de Persona y
agrega funcionalidades específicas para la gestión de pacientes.
"""

from typing import List, Optional

from persona import Persona
<<<<<<< Updated upstream
from schemas import PacienteIn
from cita import Cita, CitaIn
=======
from schemas import PacienteIn, CitaIn
from cita import Cita
from pydantic import ValidationError

>>>>>>> Stashed changes

class Paciente(Persona):
    """
    Clase para representar un paciente en el sistema hospitalario.
    
    Esta clase hereda de Persona y agrega funcionalidades específicas
    para la gestión de pacientes, incluyendo citas médicas.
    
    Attributes:
        _citas: Lista de citas del paciente
        _diagnosticos: Lista de diagnósticos del paciente
        _facturas: Lista de facturas del paciente
    """
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str) -> None:
        """
        Inicializa una nueva instancia de Paciente.
        
        Args:
            nombre: Nombre completo del paciente
            fecha_nac: Fecha de nacimiento en formato dd/mm/yyyy
            telefono: Número de teléfono
            direccion: Dirección de residencia
        """
        super().__init__(nombre, fecha_nac, telefono, direccion)
<<<<<<< Updated upstream
        self._tipo = "Paciente"
        self._citas = []  # Lista de citas del paciente
=======
        self._tipo: str = "Paciente"
        self._citas: List[Cita] = []
        self._diagnosticos: List = []
        self._facturas: List = []
>>>>>>> Stashed changes
    
    @classmethod
    def registrar(cls) -> 'Paciente':
        """
        Método de clase para registrar un nuevo paciente.
        
        Este método solicita los datos del paciente al usuario,
        valida la entrada usando Pydantic y retorna una nueva
        instancia de Paciente.
        
        Returns:
            Paciente: Nueva instancia de paciente registrada
            
        Raises:
            ValidationError: Si los datos ingresados son inválidos
        """
        print("\n--- REGISTRAR NUEVO PACIENTE ---")
        
        nombre: str = input("Nombre: ").strip()
        fecha_nac: str = input("Fecha de nacimiento (dd/mm/yyyy): ").strip()
        telefono: str = input("Teléfono: ").strip()
        direccion: str = input("Dirección: ").strip()
        
        datos = PacienteIn(
            nombre=nombre,
            fecha_nac=fecha_nac,
            telefono=telefono,
            direccion=direccion,
        ).model_dump()
        
<<<<<<< Updated upstream
        return cls(datos["nombre"], datos["fecha_nac"], datos["telefono"], datos["direccion"])    
    
    def agendar_cita(self, medico, fecha: str, hora: str, motivo: str):
        """El paciente agenda una cita"""
=======
        return cls(
            datos["nombre"], 
            datos["fecha_nac"], 
            datos["telefono"], 
            datos["direccion"]
        )
    
    def agendar_cita(self, medico, fecha: str, hora: str, motivo: str) -> Cita:
        """
        Agenda una cita con un médico.
        
        Args:
            medico: Médico con quien se agenda la cita
            fecha: Fecha de la cita en formato dd/mm/yyyy
            hora: Hora de la cita en formato HH:MM
            motivo: Motivo de la consulta
            
        Returns:
            Cita: Nueva cita creada
            
        Raises:
            ValidationError: Si los datos son inválidos
            ValueError: Si hay conflictos de horario
        """
>>>>>>> Stashed changes
        # Validar datos de entrada
        datos_cita = CitaIn(fecha=fecha, hora=hora, motivo=motivo).model_dump()
        
        # Verificar disponibilidad del médico
        if not Cita.verificar_disponibilidad(medico, datos_cita["fecha"], datos_cita["hora"]):
            raise ValueError(f"El Dr. {medico._nombre} no está disponible en {datos_cita['fecha']} a las {datos_cita['hora']}")
        
        # Verificar que el paciente no tenga otra cita en ese horario
        if not Cita.verificar_disponibilidad_paciente(self, datos_cita["fecha"], datos_cita["hora"]):
            raise ValueError(f"Ya tienes una cita agendada en {datos_cita['fecha']} a las {datos_cita['hora']}")
        
        # Crear la cita
        cita = Cita(self, medico, datos_cita["fecha"], datos_cita["hora"], datos_cita["motivo"])
        
        # Agregar a las listas de ambos
        self._citas.append(cita)
        if not hasattr(medico, '_citas'):
            medico._citas = []
        medico._citas.append(cita)
        
        return cita
    
<<<<<<< Updated upstream
    def ver_citas(self):
        """Muestra todas las citas del paciente"""
=======
    def ver_citas(self) -> None:
        """
        Muestra todas las citas del paciente.
        
        Este método imprime en consola todas las citas
        agendadas del paciente.
        """
>>>>>>> Stashed changes
        if not self._citas:
            print(f"\n{self._nombre} no tiene citas agendadas")
            return
        
        print(f"\n--- CITAS DE {self._nombre.upper()} ---")
        for cita in self._citas:
            cita.mostrar_cita()
            print("-" * 30)
    
<<<<<<< Updated upstream
    def cancelar_cita(self, fecha: str, hora: str):
        """Cancela una cita específica"""
        for cita in self._citas:
            if cita.fecha == fecha and cita.hora == hora and cita.estado == "Agendada":
                cita.estado = "Cancelada"
                print(f"Cita cancelada exitosamente para {fecha} a las {hora}")
                return
        
        print("No se encontró una cita agendada para esa fecha y hora")
=======
    def cancelar_cita(self, fecha: str, hora: str) -> bool:
        """
        Cancela una cita específica.
        
        Args:
            fecha: Fecha de la cita a cancelar
            hora: Hora de la cita a cancelar
            
        Returns:
            bool: True si la cita fue cancelada exitosamente, False en caso contrario
        """
        for cita in self._citas:
            if cita.fecha == fecha and cita.hora == hora and cita.estado == "Agendada":
                cita.cancelar()
                print(f"Cita cancelada exitosamente para {fecha} a las {hora}")
                return True
        
        print("No se encontró una cita agendada para esa fecha y hora")
        return False
    
    def obtener_citas_agendadas(self) -> List[Cita]:
        """
        Obtiene todas las citas agendadas del paciente.
        
        Returns:
            List[Cita]: Lista de citas agendadas
        """
        return [cita for cita in self._citas if cita.estado == "Agendada"]
    
    def obtener_citas_canceladas(self) -> List[Cita]:
        """
        Obtiene todas las citas canceladas del paciente.
        
        Returns:
            List[Cita]: Lista de citas canceladas
        """
        return [cita for cita in self._citas if cita.estado == "Cancelada"]
    
    def obtener_citas_completadas(self) -> List[Cita]:
        """
        Obtiene todas las citas completadas del paciente.
        
        Returns:
            List[Cita]: Lista de citas completadas
        """
        return [cita for cita in self._citas if cita.estado == "Completada"]
    
    def obtener_info_especifica(self) -> str:
        """
        Obtiene información específica del paciente.
        
        Returns:
            str: Información específica del paciente
        """
        citas_agendadas: int = len(self.obtener_citas_agendadas())
        return f"Paciente con {citas_agendadas} citas agendadas"
>>>>>>> Stashed changes
    
    def mostrardatos(self) -> None:
        """
        Muestra los datos del paciente.
        
        Este método imprime en consola toda la información
        del paciente incluyendo estadísticas de citas.
        """
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()
<<<<<<< Updated upstream
        print(f"Citas agendadas: {len([c for c in self._citas if c.estado == 'Agendada'])}")
=======
        citas_agendadas: int = len(self.obtener_citas_agendadas())
        print(f"Citas agendadas: {citas_agendadas}")
    
    def __str__(self) -> str:
        """
        Retorna una representación en string del paciente.
        
        Returns:
            str: Representación del paciente
        """
        return f"Paciente: {self._nombre}"
    
    def __repr__(self) -> str:
        """
        Retorna una representación técnica del paciente.
        
        Returns:
            str: Representación técnica del paciente
        """
        return f"Paciente(nombre='{self._nombre}', fecha_nac='{self._fecha_nac}')"
>>>>>>> Stashed changes



