"""
Clase para gestionar médicos en el Sistema Hospitalario.

Este módulo contiene la clase Medico que hereda de Persona y
agrega funcionalidades específicas para la gestión de médicos,
incluyendo diagnósticos y facturas.
"""

from datetime import datetime
from typing import List, Optional

from persona import Persona
<<<<<<< Updated upstream
from schemas import MedicoIn
from cita import Cita, CitaIn
=======
from schemas import MedicoIn, DiagnosticoIn, FacturaIn, CitaIn
from cita import Cita
from pydantic import ValidationError


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
        print(f"--- FACTURA MÉDICA ---")
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

>>>>>>> Stashed changes

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
            telefono: Número de teléfono
            direccion: Dirección de residencia
            especialidad: Especialidad médica
        """
        super().__init__(nombre, fecha_nac, telefono, direccion)
<<<<<<< Updated upstream
        self._especialidad = especialidad
        self._tipo = "Médico"
        self._citas = []  # Lista de citas del médico
=======
        self._especialidad: str = especialidad
        self._tipo: str = "Médico"
        self._citas: List[Cita] = []
        self._diagnosticos: List[Diagnostico] = []
        self._facturas: List[Factura] = []
>>>>>>> Stashed changes
    
    @classmethod
    def registrar(cls) -> 'Medico':
        """
        Método de clase para registrar un nuevo médico.
        
        Este método solicita los datos del médico al usuario,
        valida la entrada usando Pydantic y retorna una nueva
        instancia de Medico.
        
        Returns:
            Medico: Nueva instancia de médico registrado
            
        Raises:
            ValidationError: Si los datos ingresados son inválidos
        """
        print("\n--- REGISTRAR NUEVO MÉDICO ---")
        
        nombre: str = input("Nombre: ").strip()
        fecha_nac: str = input("Fecha de nacimiento (dd/mm/yyyy): ").strip()
        telefono: str = input("Teléfono: ").strip()
        direccion: str = input("Dirección: ").strip()
        especialidad: str = input("Especialidad: ").strip()
        
        datos = MedicoIn(
            nombre=nombre,
            fecha_nac=fecha_nac,
            telefono=telefono,
            direccion=direccion,
            especialidad=especialidad,
        ).model_dump()
        
<<<<<<< Updated upstream
        return cls(datos["nombre"], datos["fecha_nac"], datos["telefono"], datos["direccion"], datos["especialidad"])    
    
    def agendar_cita_paciente(self, paciente, fecha: str, hora: str, motivo: str):
        """El médico agenda cita para un paciente"""
=======
        return cls(
            datos["nombre"], 
            datos["fecha_nac"], 
            datos["telefono"], 
            datos["direccion"], 
            datos["especialidad"]
        )
    
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
            ValidationError: Si los datos son inválidos
            ValueError: Si hay conflictos de horario
        """
>>>>>>> Stashed changes
        # Validar datos de entrada
        datos_cita = CitaIn(fecha=fecha, hora=hora, motivo=motivo).model_dump()
        
        # Verificar disponibilidad del médico
        if not Cita.verificar_disponibilidad(self, datos_cita["fecha"], datos_cita["hora"]):
            raise ValueError(f"No estás disponible en {datos_cita['fecha']} a las {datos_cita['hora']}")
        
        # Verificar que el paciente no tenga otra cita en ese horario
        if not Cita.verificar_disponibilidad_paciente(paciente, datos_cita["fecha"], datos_cita["hora"]):
            raise ValueError(f"El paciente {paciente._nombre} ya tiene una cita en {datos_cita['fecha']} a las {datos_cita['hora']}")
        
        # Crear la cita
        cita = Cita(paciente, self, datos_cita["fecha"], datos_cita["hora"], datos_cita["motivo"])
        
        # Agregar a las listas de ambos
        self._citas.append(cita)
        if not hasattr(paciente, '_citas'):
            paciente._citas = []
        paciente._citas.append(cita)
        
        return cita
    
<<<<<<< Updated upstream
    def ver_citas(self):
        """Muestra todas las citas del médico"""
=======
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
            ValidationError: Si los datos son inválidos
        """
        # Validar datos de entrada
        datos_diagnostico = DiagnosticoIn(
            sintomas=sintomas,
            diagnostico=diagnostico,
            tratamiento=tratamiento,
            observaciones=observaciones,
            fecha_diagnostico=fecha_diagnostico or datetime.now().strftime("%d/%m/%Y")
        ).model_dump()
        
        # Crear el diagnóstico
        diagnostico_obj = Diagnostico(
            paciente=paciente,
            medico=self,
            sintomas=datos_diagnostico["sintomas"],
            diagnostico=datos_diagnostico["diagnostico"],
            tratamiento=datos_diagnostico["tratamiento"],
            observaciones=datos_diagnostico["observaciones"],
            fecha_diagnostico=datos_diagnostico["fecha_diagnostico"]
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
>>>>>>> Stashed changes
        if not self._citas:
            print(f"\nEl Dr. {self._nombre} no tiene citas agendadas")
            return
        
        print(f"\n--- CITAS DEL DR. {self._nombre.upper()} ---")
        for cita in self._citas:
            cita.mostrar_cita()
            print("-" * 30)
    
<<<<<<< Updated upstream
    def ver_citas_por_fecha(self, fecha: str):
        """Muestra las citas del médico en una fecha específica"""
        citas_fecha = [c for c in self._citas if c.fecha == fecha and c.estado == "Agendada"]
=======
    def ver_citas_por_fecha(self, fecha: str) -> None:
        """
        Muestra las citas del médico en una fecha específica.
        
        Args:
            fecha: Fecha para filtrar las citas
        """
        citas_fecha: List[Cita] = [c for c in self._citas if c.fecha == fecha and c.estado == "Agendada"]
>>>>>>> Stashed changes
        
        if not citas_fecha:
            print(f"\nNo hay citas agendadas para el {fecha}")
            return
        
        print(f"\n--- CITAS DEL DR. {self._nombre.upper()} PARA {fecha} ---")
        for cita in citas_fecha:
            cita.mostrar_cita()
            print("-" * 30)
    
<<<<<<< Updated upstream
    def cancelar_cita(self, fecha: str, hora: str):
        """Cancela una cita específica"""
        for cita in self._citas:
            if cita.fecha == fecha and cita.hora == hora and cita.estado == "Agendada":
                cita.estado = "Cancelada"
                print(f"Cita cancelada exitosamente para {fecha} a las {hora}")
                return
        
        print("No se encontró una cita agendada para esa fecha y hora")
=======
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
>>>>>>> Stashed changes
    
    def mostrardatos(self) -> None:
        """
        Muestra los datos del médico.
        
        Este método imprime en consola toda la información
        del médico incluyendo estadísticas de citas, diagnósticos y facturas.
        """
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()
        print(f"Especialidad: {self._especialidad}")
<<<<<<< Updated upstream
        print(f"Citas agendadas: {len([c for c in self._citas if c.estado == 'Agendada'])}")
=======
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
>>>>>>> Stashed changes
