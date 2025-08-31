class Persona:
    """Clase padre para todas las personas del hospital"""
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str):
        self._nombre = nombre
        self._fecha_nac = fecha_nac
        self._telefono = telefono
        self._direccion = direccion
    
    def mostrardatos(self) -> None:
        """Muestra todos los datos de la persona"""
        print(f"Nombre: {self._nombre}")
        print(f"Fecha de nacimiento: {self._fecha_nac}")
        print(f"Teléfono: {self._telefono}")
        print(f"Dirección: {self._direccion}")
