from typing import List, Optional
from datetime import datetime
from persona import Persona
from schemas import EnfermeraIn, FacturaIn, Turno, validar_campo_nombre, validar_campo_fecha, validar_campo_telefono, validar_campo_direccion, validar_campo_concepto, validar_campo_monto, validar_campo_tipo_servicio, validar_campo_fecha_servicio, validar_campo_descripcion

class Factura:
    """
    Clase para gestionar facturas de servicios de enfermería.
    
    Esta clase encapsula toda la información relacionada con
    una factura emitida por servicios de enfermería.
    
    Attributes:
        paciente: Paciente facturado
        enfermera: Enfermera que emitió la factura
        concepto: Concepto del servicio
        monto: Monto del servicio
        tipo_servicio: Tipo de servicio prestado
        fecha_servicio: Fecha del servicio
        descripcion: Descripción detallada del servicio
        numero_factura: Número único de factura
        fecha_emision: Fecha y hora de emisión
    """
    
    def __init__(self, paciente, enfermera, concepto: str, monto: float, 
                 tipo_servicio: str, fecha_servicio: str, descripcion: str = "") -> None:
        """
        Inicializa una nueva instancia de Factura.
        
        Args:
            paciente: Paciente facturado
            enfermera: Enfermera que emitió la factura
            concepto: Concepto del servicio
            monto: Monto del servicio
            tipo_servicio: Tipo de servicio prestado
            fecha_servicio: Fecha del servicio
            descripcion: Descripción detallada del servicio
        """
        self.paciente = paciente
        self.enfermera = enfermera
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
        return f"FAC-ENF-{timestamp}"
    
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
        print(f"Enfermera: {self.enfermera._nombre}")
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
    
    Esta clase hereda de Persona y agrega funcionalidades específicas
    para la gestión de enfermeras, incluyendo turnos y facturación.
    
    Attributes:
        _turno: Turno de trabajo de la enfermera
        _facturas: Lista de facturas emitidas por la enfermera
    """
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str, turno: str) -> None:
        """
        Inicializa una nueva instancia de Enfermera.
        
        Args:
            nombre: Nombre completo de la enfermera
            fecha_nac: Fecha de nacimiento en formato dd/mm/yyyy
            telefono: Número de teléfono de contacto
            direccion: Dirección de residencia
            turno: Turno de trabajo de la enfermera
        """
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._turno: str = turno
        self._tipo: str = "Enfermera"
        self._facturas: List[Factura] = []
    
    @classmethod
    def registrar(cls) -> 'Enfermera':
        """
        Método de clase para registrar una nueva enfermera con validación campo por campo.
        
        Este método solicita los datos de la enfermera al usuario,
        valida la entrada campo por campo usando Pydantic y retorna una nueva
        instancia de Enfermera.
        
        Returns:
            Enfermera: Nueva instancia de enfermera registrada
            
        Raises:
            ValueError: Si los datos ingresados son inválidos
        """
        print("\n--- REGISTRAR NUEVA ENFERMERA ---")
        
        # Validar nombre
        while True:
            nombre: str = input("Nombre: ").strip()
            es_valido, mensaje = validar_campo_nombre(nombre)
            if es_valido:
                break
            else:
                print(f"   • {mensaje}")
                print("   Por favor, corrija el nombre.\n")
        
        # Validar fecha de nacimiento
        while True:
            fecha_nac: str = input("Fecha de nacimiento (dd/mm/yyyy): ").strip()
            es_valido, mensaje = validar_campo_fecha(fecha_nac)
            if es_valido:
                break
            else:
                print(f"   • {mensaje}")
                print("   Por favor, corrija la fecha.\n")
        
        # Validar teléfono
        while True:
            telefono: str = input("Teléfono: ").strip()
            es_valido, mensaje = validar_campo_telefono(telefono)
            if es_valido:
                break
            else:
                print(f"   • {mensaje}")
                print("   Por favor, corrija el teléfono.\n")
        
        # Validar dirección
        while True:
            direccion: str = input("Dirección: ").strip()
            es_valido, mensaje = validar_campo_direccion(direccion)
            if es_valido:
                break
            else:
                print(f"   • {mensaje}")
                print("   Por favor, corrija la dirección.\n")
        
        # Validar turno
        while True:
            print("Turnos disponibles:")
            for i, turno in enumerate(Turno, 1):
                print(f"{i}. {turno.value}")
            
            turno_opcion: str = input("Seleccione turno (número): ").strip()
            try:
                turno_idx: int = int(turno_opcion) - 1
                if 0 <= turno_idx < len(Turno):
                    turno: str = list(Turno)[turno_idx].value
                else:
                    raise ValueError("Opción de turno inválida")
            except ValueError:
                print("   • Debe seleccionar un número válido de turno")
                print("   Por favor, seleccione un turno válido.\n")
                continue
            
            # Validar turno usando Pydantic
            try:
                EnfermeraIn(nombre="test", fecha_nac="01/01/1990", telefono="1234567", direccion="test", turno=Turno(turno))
                # Crear la enfermera con datos validados
                return cls(nombre, fecha_nac, telefono, direccion, turno)
            except ValueError:
                print("   • Turno inválido")
                print("   Por favor, seleccione un turno válido.\n")
    
    def emitir_factura(self, paciente, concepto: str, monto: float, tipo_servicio: str, 
                      fecha_servicio: str, descripcion: str = "") -> Factura:
        """
        Emite una factura por servicios de enfermería prestados.
        
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
            ValueError: Si los datos son inválidos
        """
        # Validar datos de entrada
        es_valido_concepto, mensaje_concepto = validar_campo_concepto(concepto)
        if not es_valido_concepto:
            raise ValueError(f"Concepto: {mensaje_concepto}")
        
        es_valido_monto, mensaje_monto = validar_campo_monto(monto)
        if not es_valido_monto:
            raise ValueError(f"Monto: {mensaje_monto}")
        
        es_valido_tipo, mensaje_tipo = validar_campo_tipo_servicio(tipo_servicio)
        if not es_valido_tipo:
            raise ValueError(f"Tipo de servicio: {mensaje_tipo}")
        
        es_valido_fecha, mensaje_fecha = validar_campo_fecha_servicio(fecha_servicio)
        if not es_valido_fecha:
            raise ValueError(f"Fecha del servicio: {mensaje_fecha}")
        
        es_valido_desc, mensaje_desc = validar_campo_descripcion(descripcion)
        if not es_valido_desc:
            raise ValueError(f"Descripción: {mensaje_desc}")
        
        # Crear la factura
        factura: Factura = Factura(
            paciente=paciente,
            enfermera=self,
            concepto=concepto,
            monto=monto,
            tipo_servicio=tipo_servicio,
            fecha_servicio=fecha_servicio,
            descripcion=descripcion
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
        emitidas por la enfermera de forma legible.
        """
        if not self._facturas:
            print(f"\n{self._nombre} no tiene facturas emitidas")
            return
        
        print(f"\n--- FACTURAS EMITIDAS POR {self._nombre.upper()} ---")
        for factura in self._facturas:
            factura.mostrar_factura()
            print("-" * 30)
    
    def obtener_info_especifica(self) -> str:
        """
        Obtiene información específica de la enfermera.
        
        Returns:
            str: Información específica de la enfermera
        """
        facturas: int = len(self._facturas)
        return f"Enfermera de turno {self._turno} con {facturas} facturas emitidas"
    
    def mostrar_datos(self) -> None:
        """
        Muestra los datos de la enfermera.
        
        Este método imprime en consola toda la información
        de la enfermera incluyendo estadísticas de facturas.
        """
        print(f"--- {self._tipo.upper()} ---")
        super().mostrar_datos()
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
