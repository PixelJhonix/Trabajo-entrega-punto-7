from persona import Persona

class Paciente(Persona):
    """Clase para pacientes del hospital"""
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str):
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._tipo = "Paciente"
    
    @classmethod
    def registrar(cls):
        """Método de clase para registrar un nuevo paciente"""
        print("\n--- REGISTRAR NUEVO PACIENTE ---")
        
        nombre = input("Nombre: ")
        fecha_nac = input("Fecha de nacimiento (dd/mm/yyyy): ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        
        return cls(nombre, fecha_nac, telefono, direccion)
    
    def mostrardatos(self) -> None:
        """Muestra datos del paciente"""
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()



