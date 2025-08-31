from persona import Persona
from schemas import MedicoIn
from cita import Cita, CitaIn

class Medico(Persona):
    """Clase para médicos del hospital"""
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str, especialidad: str):
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._especialidad = especialidad
        self._tipo = "Médico"
        self._citas = []  # Lista de citas del médico
    
    @classmethod
    def registrar(cls):
        """Método de clase para registrar un nuevo médico"""
        print("\n--- REGISTRAR NUEVO MÉDICO ---")
        
        nombre = input("Nombre: ")
        fecha_nac = input("Fecha de nacimiento (dd/mm/yyyy): ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        especialidad = input("Especialidad: ")
        
        datos = MedicoIn(
            nombre=nombre,
            fecha_nac=fecha_nac,
            telefono=telefono,
            direccion=direccion,
            especialidad=especialidad,
        ).model_dump()
        
        return cls(datos["nombre"], datos["fecha_nac"], datos["telefono"], datos["direccion"], datos["especialidad"])    
    
    def agendar_cita_paciente(self, paciente, fecha: str, hora: str, motivo: str):
        """El médico agenda cita para un paciente"""
        # Validar datos de entrada
        datos_cita = CitaIn(fecha=fecha, hora=hora, motivo=motivo).model_dump()
        
        # Verificar disponibilidad del médico
        if not Cita.verificar_disponibilidad(self, datos_cita["fecha"], datos_cita["hora"]):
            raise ValueError(f"No estás disponible en {datos_cita['fecha']} a las {datos_cita['hora']}")
        
        # Verificar que el paciente no tenga otra cita en ese horario
        if not Cita.verificar_disponibilidad_paciente(paciente, datos_cita["fecha"], datos_cita["hora"]):
            raise ValueError(f"El paciente {paciente._nombre} ya tiene una cita en {datos_cita['fecha']} a las {datos_cita['hora']}")
        
        # Crear la cita
        cita = Cita(paciente, self, datos_cita["fecha"], datos_cita["hora"], datos_cita["motivo"])
        
        # Agregar a las listas de ambos
        self._citas.append(cita)
        if not hasattr(paciente, '_citas'):
            paciente._citas = []
        paciente._citas.append(cita)
        
        return cita
    
    def ver_citas(self):
        """Muestra todas las citas del médico"""
        if not self._citas:
            print(f"\nEl Dr. {self._nombre} no tiene citas agendadas")
            return
        
        print(f"\n--- CITAS DEL DR. {self._nombre.upper()} ---")
        for cita in self._citas:
            cita.mostrar_cita()
            print("-" * 30)
    
    def ver_citas_por_fecha(self, fecha: str):
        """Muestra las citas del médico en una fecha específica"""
        citas_fecha = [c for c in self._citas if c.fecha == fecha and c.estado == "Agendada"]
        
        if not citas_fecha:
            print(f"\nNo hay citas agendadas para el {fecha}")
            return
        
        print(f"\n--- CITAS DEL DR. {self._nombre.upper()} PARA {fecha} ---")
        for cita in citas_fecha:
            cita.mostrar_cita()
            print("-" * 30)
    
    def cancelar_cita(self, fecha: str, hora: str):
        """Cancela una cita específica"""
        for cita in self._citas:
            if cita.fecha == fecha and cita.hora == hora and cita.estado == "Agendada":
                cita.estado = "Cancelada"
                print(f"Cita cancelada exitosamente para {fecha} a las {hora}")
                return
        
        print("No se encontró una cita agendada para esa fecha y hora")
    
    def mostrardatos(self) -> None:
        """Muestra datos del médico"""
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()
        print(f"Especialidad: {self._especialidad}")
        print(f"Citas agendadas: {len([c for c in self._citas if c.estado == 'Agendada'])}")