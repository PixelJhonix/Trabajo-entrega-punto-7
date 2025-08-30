from persona import Persona

class Enfermera(Persona):
    """Clase para enfermeras del hospital"""
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str, turno: str):
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._turno = turno
        self._tipo = "Enfermera"
    
    @classmethod
    def registrar(cls):
        """Método de clase para registrar una nueva enfermera"""
        print("\n--- REGISTRAR NUEVA ENFERMERA ---")
        
        nombre = input("Nombre: ")
        fecha_nac = input("Fecha de nacimiento (dd/mm/yyyy): ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        turno = input("Turno (Mañana/Tarde/Noche): ")
        
        return cls(nombre, fecha_nac, telefono, direccion, turno)
    
    def mostrardatos(self) -> None:
        """Muestra datos de la enfermera"""
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()
        print(f"Turno: {self._turno}")
