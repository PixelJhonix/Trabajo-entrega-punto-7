from abc import ABC, abstractmethod
from typing import List

class Persona(ABC):
    """
    Clase base abstracta para todas las personas en el sistema hospitalario.
    
    Esta clase define la estructura común para pacientes, médicos y enfermeras,
    incluyendo atributos básicos y métodos que deben ser implementados.
    
    Attributes:
        _nombre: Nombre completo de la persona
        _fecha_nac: Fecha de nacimiento en formato dd/mm/yyyy
        _telefono: Número de teléfono de contacto
        _direccion: Dirección de residencia
        _tipo: Tipo de persona (Paciente, Médico, Enfermera)
    """
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str) -> None:
        """
        Inicializa una nueva instancia de Persona.
        
        Args:
            nombre: Nombre completo de la persona
            fecha_nac: Fecha de nacimiento en formato dd/mm/yyyy
            telefono: Número de teléfono de contacto
            direccion: Dirección de residencia
        """
        self._nombre: str = nombre
        self._fecha_nac: str = fecha_nac
        self._telefono: str = telefono
        self._direccion: str = direccion
        self._tipo: str = "Persona"
    
    @property
    def nombre(self) -> str:
        """Obtiene el nombre de la persona"""
        return self._nombre
    
    @property
    def fecha_nac(self) -> str:
        """Obtiene la fecha de nacimiento de la persona"""
        return self._fecha_nac
    
    @property
    def telefono(self) -> str:
        """Obtiene el teléfono de la persona"""
        return self._telefono
    
    @property
    def direccion(self) -> str:
        """Obtiene la dirección de la persona"""
        return self._direccion
    
    @property
    def tipo(self) -> str:
        """Obtiene el tipo de persona"""
        return self._tipo
    
    def mostrar_datos(self) -> None:
        """
        Muestra todos los datos básicos de la persona.
        
        Este método imprime en consola la información básica
        de la persona de forma legible.
        """
        print(f"Nombre: {self._nombre}")
        print(f"Fecha de nacimiento: {self._fecha_nac}")
        print(f"Teléfono: {self._telefono}")
        print(f"Dirección: {self._direccion}")
    
    @abstractmethod
    def obtener_info_especifica(self) -> str:
        """
        Método abstracto para obtener información específica de cada tipo de persona.
        
        Returns:
            str: Información específica de la persona
        """
        pass
    
    def __str__(self) -> str:
        """
        Retorna una representación en string de la persona.
        
        Returns:
            str: Representación de la persona
        """
        return f"{self._tipo}: {self._nombre}"
    
    def __repr__(self) -> str:
        """
        Retorna una representación técnica de la persona.
        
        Returns:
            str: Representación técnica de la persona
        """
        return f"{self.__class__.__name__}(nombre='{self._nombre}', tipo='{self._tipo}')"
