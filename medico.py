"""
Clase para gestionar médicos en el Sistema Hospitalario.

Este módulo contiene la clase Medico que hereda de Persona y
agrega funcionalidades específicas para la gestión de médicos,
incluyendo diagnósticos, facturas y citas.
"""

from datetime import datetime
from typing import List, Optional
from persona import Persona
from schemas import MedicoIn, DiagnosticoIn, FacturaIn, CitaIn, validar_campo_nombre, validar_campo_fecha, validar_campo_telefono, validar_campo_direccion, validar_campo_especialidad, validar_campo_concepto, validar_campo_monto, validar_campo_tipo_servicio, validar_campo_fecha_servicio, validar_campo_descripcion, validar_campo_sintomas, validar_campo_diagnostico, validar_campo_tratamiento, validar_campo_observaciones, validar_campo_motivo, validar_campo_hora
from cita import Cita


class Diagnostico:
    """
    Clase para gestionar diagnósticos médicos.
    
    Esta clase encapsula toda la información relacionada con
    un diagnóstico médico realizado a un paciente.
    
    Attributes:
        paciente: Paciente diagnosticado
        medico: Médico que realizó el diagnóstico
        sintomas: Descripción de los síntomas
        diagnostico: Diagnóstico médico
        tratamiento: Tratamiento prescrito
        observaciones: Observaciones adicionales
        fecha_diagnostico: Fecha del diagnóstico
        fecha_creacion: Fecha y hora de creación del registro
    """
    
    def __init__(self, paciente, medico, sintomas: str, diagnostico: str, 
                 tratamiento: str, observaciones: str = "", fecha_diagnostico: str = None) -> None:
        """
        Inicializa una nueva instancia de Diagnostico.
        
        Args:
            paciente: Paciente diagnosticado
            medico: Médico que realizó el diagnóstico
            sintomas: Descripción de los síntomas
            diagnostico: Diagnóstico médico
            tratamiento: Tratamiento prescrito
            observaciones: Observaciones adicionales
            fecha_diagnostico: Fecha del diagnóstico
        """
        self.paciente = paciente
        self.medico = medico
        self.sintomas: str = sintomas
        self.diagnostico: str = diagnostico
        self.tratamiento: str = tratamiento
        self.observaciones: str = observaciones
        self.fecha_diagnostico: str = fecha_diagnostico or datetime.now().strftime("%d/%m/%Y")
        self.fecha_creacion: datetime = datetime.now()
    
    def mostrar_diagnostico(self) -> None:
        """
        Muestra los detalles del diagnóstico.
        
        Este método imprime en consola toda la información
        relacionada con el diagnóstico de forma legible.
        """
        print(f"--- DIAGNÓSTICO MÉDICO ---")
        print(f"Paciente: {self.paciente._nombre}")
        print(f"Médico: Dr. {self.medico._nombre}")
        print(f"Fecha: {self.fecha_diagnostico}")
        print(f"Síntomas: {self.sintomas}")
        print(f"Diagnóstico: {self.diagnostico}")
        print(f"Tratamiento: {self.tratamiento}")
        if self.observaciones:
            print(f"Observaciones: {self.observaciones}")
        print(f"Fecha de registro: {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}")


class Factura:
    """
    Clase para gestionar facturas médicas.
    
    Esta clase encapsula toda la información relacionada con
    una factura emitida por servicios médicos.
    
    Attributes:
        paciente: Paciente facturado
        medico: Médico que emitió la factura
        concepto: Concepto del servicio
        monto: Monto del servicio
        tipo_servicio: Tipo de servicio prestado
        fecha_servicio: Fecha del servicio
        descripcion: Descripción detallada del servicio
        numero_factura: Número único de factura
        fecha_emision: Fecha y hora de emisión
    """
    
    def __init__(self, paciente, medico, concepto: str, monto: float, 
                 tipo_servicio: str, fecha_servicio: str, descripcion: str = "") -> None:
        """
        Inicializa una nueva instancia de Factura.
        
        Args:
            paciente: Paciente facturado
            medico: Médico que emitió la factura
            concepto: Concepto del servicio
            monto: Monto del servicio
            tipo_servicio: Tipo de servicio prestado
            fecha_servicio: Fecha del servicio
            descripcion: Descripción detallada del servicio
        """
        self.paciente = paciente
        self.medico = medico
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
        return f"FAC-MED-{timestamp}"
    
    def mostrar_factura(self) -> None:
        """
        Muestra los detalles de la factura.
        
        Este método imprime en consola toda la información
        relacionada con la factura de forma legible.
        """
        print(f"--- FACTURA MÉDICA ---")
        print(f"Número: {self.numero_factura}")
        print(f"Fecha de emisión: {self.fecha_emision.strftime('%d/%m/%Y %H:%M')}")
        print(f"Paciente: {self.paciente._nombre}")
        print(f"Médico: Dr. {self.medico._nombre}")
        print(f"Concepto: {self.concepto}")
        print(f"Tipo de servicio: {self.tipo_servicio}")
        print(f"Fecha del servicio: {self.fecha_servicio}")
        if self.descripcion:
            print(f"Descripción: {self.descripcion}")
        print(f"Monto: ${self.monto:,.2f}")
        print("-" * 30)


class Medico(Persona):
    """
    Clase para representar un médico en el sistema hospitalario.
    
    Esta clase hereda de Persona y agrega funcionalidades específicas
    para la gestión de médicos, incluyendo diagnósticos, facturas y citas.
    
    Attributes:
        _especialidad: Especialidad médica del doctor
        _citas: Lista de citas del médico
        _diagnosticos: Lista de diagnósticos realizados
        _facturas: Lista de facturas emitidas
    """
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str, especialidad: str) -> None:
        """
        Inicializa una nueva instancia de Medico.
        
        Args:
            nombre: Nombre completo del médico
            fecha_nac: Fecha de nacimiento en formato dd/mm/yyyy
            telefono: Número de teléfono de contacto
            direccion: Dirección de residencia
            especialidad: Especialidad médica
        """
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._especialidad: str = especialidad
        self._tipo: str = "Médico"
        self._citas: List[Cita] = []
        self._diagnosticos: List[Diagnostico] = []
        self._facturas: List[Factura] = []
    
    @classmethod
    def registrar(cls) -> 'Medico':
        """
        Método de clase para registrar un nuevo médico con validación campo por campo.
        
        Este método solicita los datos del médico al usuario,
        valida la entrada campo por campo usando Pydantic y retorna una nueva
        instancia de Medico.
        
        Returns:
            Medico: Nueva instancia de médico registrado
            
        Raises:
            ValueError: Si los datos ingresados son inválidos
        """
        print("\n--- REGISTRAR NUEVO MÉDICO ---")
        
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
        
        # Validar especialidad
        while True:
            especialidad: str = input("Especialidad: ").strip()
            es_valido, mensaje = validar_campo_especialidad(especialidad)
            if es_valido:
                # Crear el médico con datos validados
                return cls(nombre, fecha_nac, telefono, direccion, especialidad)
            else:
                print(f"   • {mensaje}")
                print("   Por favor, corrija la especialidad.\n")
    
    def agendar_cita_paciente(self, paciente, fecha: str, hora: str, motivo: str) -> Cita:
        """
        Agenda una cita para un paciente.
        
        Args:
            paciente: Paciente para quien se agenda la cita
            fecha: Fecha de la cita en formato dd/mm/yyyy
            hora: Hora de la cita en formato HH:MM
            motivo: Motivo de la consulta
            
        Returns:
            Cita: Nueva cita creada
            
        Raises:
            ValueError: Si los datos son inválidos o hay conflictos de horario
        """
        # Validar datos de entrada
        es_valido_fecha, mensaje_fecha = validar_campo_fecha_servicio(fecha)
        if not es_valido_fecha:
            raise ValueError(f"Fecha: {mensaje_fecha}")
        
        es_valido_hora, mensaje_hora = validar_campo_hora(hora)
        if not es_valido_hora:
            raise ValueError(f"Hora: {mensaje_hora}")
        
        es_valido_motivo, mensaje_motivo = validar_campo_motivo(motivo)
        if not es_valido_motivo:
            raise ValueError(f"Motivo: {mensaje_motivo}")
        
        # Verificar disponibilidad del médico
        if not Cita.verificar_disponibilidad(self, fecha, hora):
            raise ValueError(f"No estás disponible en {fecha} a las {hora}")
        
        # Verificar que el paciente no tenga otra cita en ese horario
        if not Cita.verificar_disponibilidad_paciente(paciente, fecha, hora):
            raise ValueError(f"El paciente {paciente._nombre} ya tiene una cita en {fecha} a las {hora}")
        
        # Crear la cita
        cita: Cita = Cita(paciente, self, fecha, hora, motivo)
        
        # Agregar a las listas de ambos
        self._citas.append(cita)
        if not hasattr(paciente, '_citas'):
            paciente._citas = []
        paciente._citas.append(cita)
        
        return cita
    
    def registrar_diagnostico(self, paciente, sintomas: str, diagnostico: str, 
                             tratamiento: str, observaciones: str = "", 
                             fecha_diagnostico: str = None) -> Diagnostico:
        """
        Registra un diagnóstico para un paciente.
        
        Args:
            paciente: Paciente diagnosticado
            sintomas: Descripción de los síntomas
            diagnostico: Diagnóstico médico
            tratamiento: Tratamiento prescrito
            observaciones: Observaciones adicionales
            fecha_diagnostico: Fecha del diagnóstico
            
        Returns:
            Diagnostico: Nuevo diagnóstico creado
            
        Raises:
            ValueError: Si los datos son inválidos
        """
        # Validar datos de entrada
        es_valido_sintomas, mensaje_sintomas = validar_campo_sintomas(sintomas)
        if not es_valido_sintomas:
            raise ValueError(f"Síntomas: {mensaje_sintomas}")
        
        es_valido_diagnostico, mensaje_diagnostico = validar_campo_diagnostico(diagnostico)
        if not es_valido_diagnostico:
            raise ValueError(f"Diagnóstico: {mensaje_diagnostico}")
        
        es_valido_tratamiento, mensaje_tratamiento = validar_campo_tratamiento(tratamiento)
        if not es_valido_tratamiento:
            raise ValueError(f"Tratamiento: {mensaje_tratamiento}")
        
        es_valido_obs, mensaje_obs = validar_campo_observaciones(observaciones)
        if not es_valido_obs:
            raise ValueError(f"Observaciones: {mensaje_obs}")
        
        fecha_diag = fecha_diagnostico or datetime.now().strftime("%d/%m/%Y")
        es_valido_fecha, mensaje_fecha = validar_campo_fecha_servicio(fecha_diag)
        if not es_valido_fecha:
            raise ValueError(f"Fecha del diagnóstico: {mensaje_fecha}")
        
        # Crear el diagnóstico
        diagnostico_obj: Diagnostico = Diagnostico(
            paciente=paciente,
            medico=self,
            sintomas=sintomas,
            diagnostico=diagnostico,
            tratamiento=tratamiento,
            observaciones=observaciones,
            fecha_diagnostico=fecha_diag
        )
        
        # Agregar a las listas de ambos
        self._diagnosticos.append(diagnostico_obj)
        if not hasattr(paciente, '_diagnosticos'):
            paciente._diagnosticos = []
        paciente._diagnosticos.append(diagnostico_obj)
        
        return diagnostico_obj
    
    def emitir_factura(self, paciente, concepto: str, monto: float, tipo_servicio: str, 
                      fecha_servicio: str, descripcion: str = "") -> Factura:
        """
        Emite una factura por servicios prestados.
        
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
            medico=self,
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
    
    def ver_diagnosticos(self) -> None:
        """
        Muestra todos los diagnósticos del médico.
        
        Este método imprime en consola todos los diagnósticos
        realizados por el médico.
        """
        if not self._diagnosticos:
            print(f"\nEl Dr. {self._nombre} no tiene diagnósticos registrados")
            return
        
        print(f"\n--- DIAGNÓSTICOS DEL DR. {self._nombre.upper()} ---")
        for diagnostico in self._diagnosticos:
            diagnostico.mostrar_diagnostico()
            print("-" * 30)
    
    def ver_facturas(self) -> None:
        """
        Muestra todas las facturas emitidas por el médico.
        
        Este método imprime en consola todas las facturas
        emitidas por el médico.
        """
        if not self._facturas:
            print(f"\nEl Dr. {self._nombre} no tiene facturas emitidas")
            return
        
        print(f"\n--- FACTURAS EMITIDAS POR EL DR. {self._nombre.upper()} ---")
        for factura in self._facturas:
            factura.mostrar_factura()
            print("-" * 30)
    
    def ver_citas(self) -> None:
        """
        Muestra todas las citas del médico.
        
        Este método imprime en consola todas las citas
        agendadas del médico.
        """
        if not self._citas:
            print(f"\nEl Dr. {self._nombre} no tiene citas agendadas")
            return
        
        print(f"\n--- CITAS DEL DR. {self._nombre.upper()} ---")
        for cita in self._citas:
            cita.mostrar_cita()
            print("-" * 30)
    
    def ver_citas_por_fecha(self, fecha: str) -> None:
        """
        Muestra las citas del médico en una fecha específica.
        
        Args:
            fecha: Fecha para filtrar las citas
        """
        citas_fecha: List[Cita] = [c for c in self._citas if c.fecha == fecha and c.estado == "Agendada"]
        
        if not citas_fecha:
            print(f"\nNo hay citas agendadas para el {fecha}")
            return
        
        print(f"\n--- CITAS DEL DR. {self._nombre.upper()} PARA {fecha} ---")
        for cita in citas_fecha:
            cita.mostrar_cita()
            print("-" * 30)
    
    def cancelar_cita(self, fecha: str, hora: str) -> bool:
        """
        Cancela una cita específica.
        
        Args:
            fecha: Fecha de la cita a cancelar
            hora: Hora de la cita a cancelar
            
        Returns:
            bool: True si la cita fue cancelada exitosamente, False en caso contrario
        """
        for cita in self._citas:
            if cita.fecha == fecha and cita.hora == hora and cita.estado == "Agendada":
                cita.cancelar()
                print(f"Cita cancelada exitosamente para {fecha} a las {hora}")
                return True
        
        print("No se encontró una cita agendada para esa fecha y hora")
        return False
    
    def obtener_citas_agendadas(self) -> List[Cita]:
        """
        Obtiene todas las citas agendadas del médico.
        
        Returns:
            List[Cita]: Lista de citas agendadas
        """
        return [cita for cita in self._citas if cita.estado == "Agendada"]
    
    def obtener_info_especifica(self) -> str:
        """
        Obtiene información específica del médico.
        
        Returns:
            str: Información específica del médico
        """
        citas_agendadas: int = len(self.obtener_citas_agendadas())
        diagnosticos: int = len(self._diagnosticos)
        facturas: int = len(self._facturas)
        return f"Médico {self._especialidad} con {citas_agendadas} citas, {diagnosticos} diagnósticos y {facturas} facturas"
    
    def mostrar_datos(self) -> None:
        """
        Muestra los datos del médico.
        
        Este método imprime en consola toda la información
        del médico incluyendo estadísticas de citas, diagnósticos y facturas.
        """
        print(f"--- {self._tipo.upper()} ---")
        super().mostrar_datos()
        print(f"Especialidad: {self._especialidad}")
        citas_agendadas: int = len(self.obtener_citas_agendadas())
        print(f"Citas agendadas: {citas_agendadas}")
        print(f"Diagnósticos registrados: {len(self._diagnosticos)}")
        print(f"Facturas emitidas: {len(self._facturas)}")
    
    def __str__(self) -> str:
        """
        Retorna una representación en string del médico.
        
        Returns:
            str: Representación del médico
        """
        return f"Dr. {self._nombre} - {self._especialidad}"
    
    def __repr__(self) -> str:
        """
        Retorna una representación técnica del médico.
        
        Returns:
            str: Representación técnica del médico
        """
        return f"Medico(nombre='{self._nombre}', especialidad='{self._especialidad}')"