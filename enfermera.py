"""
Clase para gestionar enfermeras en el Sistema Hospitalario.

Este módulo contiene la clase Enfermera que hereda de Persona y
agrega funcionalidades específicas para la gestión de enfermeras,
incluyendo facturas.
"""

from datetime import datetime
from typing import List, Optional

from persona import Persona
<<<<<<< Updated upstream
from schemas import EnfermeraIn

class Enfermera(Persona):  
=======
from schemas import EnfermeraIn, FacturaIn
from pydantic import ValidationError


class Factura:
    """
    Clase para gestionar facturas de enfermería.
    
    Esta clase encapsula toda la información relacionada con
    una factura emitida por servicios de enfermería.
    
    Attributes:
        paciente: Paciente facturado
        profesional: Profesional que emitió la factura
        concepto: Concepto del servicio
        monto: Monto del servicio
        tipo_servicio: Tipo de servicio prestado
        fecha_servicio: Fecha del servicio
        descripcion: Descripción detallada del servicio
        numero_factura: Número único de factura
        fecha_emision: Fecha y hora de emisión
    """
    
    def __init__(self, paciente, profesional, concepto: str, monto: float, 
                 tipo_servicio: str, fecha_servicio: str, descripcion: str = "") -> None:
        """
        Inicializa una nueva instancia de Factura.
        
        Args:
            paciente: Paciente facturado
            profesional: Profesional que emitió la factura
            concepto: Concepto del servicio
            monto: Monto del servicio
            tipo_servicio: Tipo de servicio prestado
            fecha_servicio: Fecha del servicio
            descripcion: Descripción detallada del servicio
        """
        self.paciente = paciente
        self.profesional = profesional
        self.concepto: str = concepto
        self.monto: float = monto
        self.tipo_servicio: str = tipo_servicio
        self.fecha_servicio: str = fecha_servicio
        self.descripcion: str = descripcion
        self.numero_factura: str = self._generar_numero_factura()
        self.fecha_emision: datetime = datetime.now()
    
    def _generar_numero_factura(self) -> str:
        """
        Genera un número único de factura.
        
        Returns:
            str: Número único de factura
        """
        timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"FAC-{timestamp}"
    
    def mostrar_factura(self) -> None:
        """
        Muestra los detalles de la factura.
        
        Este método imprime en consola toda la información
        relacionada con la factura de forma legible.
        """
        print(f"--- FACTURA DE ENFERMERÍA ---")
        print(f"Número: {self.numero_factura}")
        print(f"Fecha de emisión: {self.fecha_emision.strftime('%d/%m/%Y %H:%M')}")
        print(f"Paciente: {self.paciente._nombre}")
        print(f"Profesional: {self.profesional._nombre}")
        print(f"Tipo de profesional: {self.profesional._tipo}")
        print(f"Concepto: {self.concepto}")
        print(f"Tipo de servicio: {self.tipo_servicio}")
        print(f"Fecha del servicio: {self.fecha_servicio}")
        if self.descripcion:
            print(f"Descripción: {self.descripcion}")
        print(f"Monto: ${self.monto:,.2f}")
        print("-" * 30)


class Enfermera(Persona):
    """
    Clase para representar una enfermera en el sistema hospitalario.
>>>>>>> Stashed changes
    
    Esta clase hereda de Persona y agrega funcionalidades específicas
    para la gestión de enfermeras, incluyendo facturas.
    
    Attributes:
        _turno: Turno de trabajo de la enfermera
        _facturas: Lista de facturas emitidas
    """
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str, turno: str) -> None:
        """
        Inicializa una nueva instancia de Enfermera.
        
        Args:
            nombre: Nombre completo de la enfermera
            fecha_nac: Fecha de nacimiento en formato dd/mm/yyyy
            telefono: Número de teléfono
            direccion: Dirección de residencia
            turno: Turno de trabajo
        """
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._turno: str = turno
        self._tipo: str = "Enfermera"
        self._facturas: List[Factura] = []
    
    @classmethod
<<<<<<< Updated upstream
    def registrar(cls):       
=======
    def registrar(cls) -> 'Enfermera':
        """
        Método de clase para registrar una nueva enfermera.
        
        Este método solicita los datos de la enfermera al usuario,
        valida la entrada usando Pydantic y retorna una nueva
        instancia de Enfermera.
        
        Returns:
            Enfermera: Nueva instancia de enfermera registrada
            
        Raises:
            ValidationError: Si los datos ingresados son inválidos
        """
>>>>>>> Stashed changes
        print("\n--- REGISTRAR NUEVA ENFERMERA ---")
        
        nombre: str = input("Nombre: ").strip()
        fecha_nac: str = input("Fecha de nacimiento (dd/mm/yyyy): ").strip()
        telefono: str = input("Teléfono: ").strip()
        direccion: str = input("Dirección: ").strip()
        turno: str = input("Turno (Mañana/Tarde/Noche): ").strip()
        
        datos = EnfermeraIn(
            nombre=nombre,
            fecha_nac=fecha_nac,
            telefono=telefono,
            direccion=direccion,
            turno=turno,
        ).model_dump()
        
<<<<<<< Updated upstream
        return cls(datos["nombre"], datos["fecha_nac"], datos["telefono"], datos["direccion"], datos["turno"])  
=======
        return cls(
            datos["nombre"], 
            datos["fecha_nac"], 
            datos["telefono"], 
            datos["direccion"], 
            datos["turno"]
        )
    
    def emitir_factura(self, paciente, concepto: str, monto: float, tipo_servicio: str, 
                      fecha_servicio: str, descripcion: str = "") -> Factura:
        """
        Emite una factura por servicios de enfermería.
        
        Args:
            paciente: Paciente facturado
            concepto: Concepto del servicio
            monto: Monto del servicio
            tipo_servicio: Tipo de servicio prestado
            fecha_servicio: Fecha del servicio
            descripcion: Descripción detallada del servicio
            
        Returns:
            Factura: Nueva factura creada
            
        Raises:
            ValidationError: Si los datos son inválidos
        """
        # Validar datos de entrada
        datos_factura = FacturaIn(
            concepto=concepto,
            monto=monto,
            tipo_servicio=tipo_servicio,
            fecha_servicio=fecha_servicio,
            descripcion=descripcion
        ).model_dump()
        
        # Crear la factura
        factura = Factura(
            paciente=paciente,
            profesional=self,
            concepto=datos_factura["concepto"],
            monto=datos_factura["monto"],
            tipo_servicio=datos_factura["tipo_servicio"],
            fecha_servicio=datos_factura["fecha_servicio"],
            descripcion=datos_factura["descripcion"]
        )
        
        # Agregar a las listas de ambos
        self._facturas.append(factura)
        if not hasattr(paciente, '_facturas'):
            paciente._facturas = []
        paciente._facturas.append(factura)
        
        return factura
    
    def ver_facturas(self) -> None:
        """
        Muestra todas las facturas emitidas por la enfermera.
        
        Este método imprime en consola todas las facturas
        emitidas por la enfermera.
        """
        if not self._facturas:
            print(f"\nLa enfermera {self._nombre} no tiene facturas emitidas")
            return
        
        print(f"\n--- FACTURAS EMITIDAS POR {self._nombre.upper()} ---")
        for factura in self._facturas:
            factura.mostrar_factura()
            print("-" * 30)
    
    def obtener_facturas(self) -> List[Factura]:
        """
        Obtiene todas las facturas emitidas por la enfermera.
        
        Returns:
            List[Factura]: Lista de facturas emitidas
        """
        return self._facturas
    
    def obtener_info_especifica(self) -> str:
        """
        Obtiene información específica de la enfermera.
        
        Returns:
            str: Información específica de la enfermera
        """
        facturas: int = len(self._facturas)
        return f"Enfermera de turno {self._turno} con {facturas} facturas emitidas"
>>>>>>> Stashed changes
    
    def mostrardatos(self) -> None:
        """
        Muestra los datos de la enfermera.
        
        Este método imprime en consola toda la información
        de la enfermera incluyendo estadísticas de facturas.
        """
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()
        print(f"Turno: {self._turno}")
        print(f"Facturas emitidas: {len(self._facturas)}")
    
    def __str__(self) -> str:
        """
        Retorna una representación en string de la enfermera.
        
        Returns:
            str: Representación de la enfermera
        """
        return f"Enfermera: {self._nombre} - Turno {self._turno}"
    
    def __repr__(self) -> str:
        """
        Retorna una representación técnica de la enfermera.
        
        Returns:
            str: Representación técnica de la enfermera
        """
        return f"Enfermera(nombre='{self._nombre}', turno='{self._turno}')"
