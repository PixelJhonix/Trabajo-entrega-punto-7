from persona import Persona
from schemas import PacienteIn
from cita import Cita, CitaIn

class Paciente(Persona):
    """Clase para pacientes del hospital"""
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str):
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._tipo = "Paciente"
        self._citas = [] 
    
    @classmethod
    def registrar(cls):
        """Método de clase para registrar un nuevo paciente"""
        print("\n--- REGISTRAR NUEVO PACIENTE ---")
        
        nombre = input("Nombre: ")
        fecha_nac = input("Fecha de nacimiento (dd/mm/yyyy): ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        
        datos = PacienteIn(
            nombre=nombre,
            fecha_nac=fecha_nac,
            telefono=telefono,
            direccion=direccion,
        ).model_dump()
        
        return cls(datos["nombre"], datos["fecha_nac"], datos["telefono"], datos["direccion"])    
    
    def agendar_cita(self, medico, fecha: str, hora: str, motivo: str):
        """El paciente agenda una cita"""
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
    
    def ver_citas(self):
        """Muestra todas las citas del paciente"""
        if not self._citas:
            print(f"\n{self._nombre} no tiene citas agendadas")
            return
        
        print(f"\n--- CITAS DE {self._nombre.upper()} ---")
        for cita in self._citas:
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
        """Muestra datos del paciente"""
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()
        print(f"Citas agendadas: {len([c for c in self._citas if c.estado == 'Agendada'])}")



