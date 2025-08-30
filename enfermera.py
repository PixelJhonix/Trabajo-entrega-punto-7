from persona import Persona
from schemas import EnfermeraIn

class Enfermera(Persona): 
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str, turno: str):
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._turno = turno
        self._tipo = "Enfermera"
    
    @classmethod
    def registrar(cls): 
        print("\n--- REGISTRAR NUEVA ENFERMERA ---")
        
        nombre = input("Nombre: ")
        fecha_nac = input("Fecha de nacimiento (dd/mm/yyyy): ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        turno = input("Turno (Mañana/Tarde/Noche): ")
        
        datos = EnfermeraIn(
            nombre=nombre,
            fecha_nac=fecha_nac,
            telefono=telefono,
            direccion=direccion,
            turno=turno,
        ).model_dump()
        
        return cls(datos["nombre"], datos["fecha_nac"], datos["telefono"], datos["direccion"], datos["turno"])
    
    def mostrardatos(self) -> None:
        """Muestra datos de la enfermera"""
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()
        print(f"Turno: {self._turno}")
