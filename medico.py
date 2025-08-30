from persona import Persona

class Medico(Persona):
    """Clase para médicos del hospital"""
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str, especialidad: str):
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._especialidad = especialidad
        self._tipo = "Médico"
    
    @classmethod
    def registrar(cls):
        """Método de clase para registrar un nuevo médico"""
        print("\n--- REGISTRAR NUEVO MÉDICO ---")
        
        nombre = input("Nombre: ")
        fecha_nac = input("Fecha de nacimiento (dd/mm/yyyy): ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        especialidad = input("Especialidad: ")
        
        return cls(nombre, fecha_nac, telefono, direccion, especialidad)
    
    def mostrardatos(self) -> None:
        """Muestra datos del médico"""
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()
        print(f"Especialidad: {self._especialidad}")