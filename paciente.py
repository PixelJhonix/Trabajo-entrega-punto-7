from typing import List, Optional
from persona import Persona
from schemas import PacienteIn, CitaIn, validar_campo_nombre, validar_campo_fecha, validar_campo_telefono, validar_campo_direccion, validar_campo_motivo, validar_campo_hora, validar_campo_fecha_servicio
from cita import Cita

class Paciente(Persona):
    """
    Clase para representar un paciente en el sistema hospitalario.
    
    Esta clase hereda de Persona y agrega funcionalidades específicas
    para la gestión de pacientes, incluyendo citas médicas.
    
    Attributes:
        _citas: Lista de citas médicas del paciente
        _diagnosticos: Lista de diagnósticos recibidos
        _facturas: Lista de facturas del paciente
    """
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str) -> None:
        """
        Inicializa una nueva instancia de Paciente.
        
        Args:
            nombre: Nombre completo del paciente
            fecha_nac: Fecha de nacimiento en formato dd/mm/yyyy
            telefono: Número de teléfono de contacto
            direccion: Dirección de residencia
        """
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._tipo: str = "Paciente"
        self._citas: List[Cita] = []
        self._diagnosticos: List = []
        self._facturas: List = []
    
    @classmethod
    def registrar(cls) -> 'Paciente':
        """
        Método de clase para registrar un nuevo paciente con validación campo por campo.
        
        Este método solicita los datos del paciente al usuario,
        valida la entrada campo por campo usando Pydantic y retorna una nueva
        instancia de Paciente.
        
        Returns:
            Paciente: Nueva instancia de paciente registrado
            
        Raises:
            ValueError: Si los datos ingresados son inválidos
        """
        print("\n--- REGISTRAR NUEVO PACIENTE ---")
        
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
                # Crear el paciente con datos validados
                return cls(nombre, fecha_nac, telefono, direccion)
            else:
                print(f"   • {mensaje}")
                print("   Por favor, corrija la dirección.\n")
    
    def agendar_cita(self, medico, fecha: str, hora: str, motivo: str) -> Cita:
        """
        Agenda una cita médica con un médico específico.
        
        Args:
            medico: Médico con quien se agenda la cita
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
        if not Cita.verificar_disponibilidad(medico, fecha, hora):
            raise ValueError(f"El Dr. {medico._nombre} no está disponible en {fecha} a las {hora}")
        
        # Verificar que el paciente no tenga otra cita en ese horario
        if not Cita.verificar_disponibilidad_paciente(self, fecha, hora):
            raise ValueError(f"Ya tienes una cita agendada en {fecha} a las {hora}")
        
        # Crear la cita
        cita: Cita = Cita(self, medico, fecha, hora, motivo)
        
        # Agregar a las listas de ambos
        self._citas.append(cita)
        if not hasattr(medico, '_citas'):
            medico._citas = []
        medico._citas.append(cita)
        
        return cita
    
    def ver_citas(self) -> None:
        """
        Muestra todas las citas del paciente.
        
        Este método imprime en consola todas las citas
        agendadas del paciente de forma legible.
        """
        if not self._citas:
            print(f"\n{self._nombre} no tiene citas agendadas")
            return
        
        print(f"\n--- CITAS DE {self._nombre.upper()} ---")
        for cita in self._citas:
            cita.mostrar_cita()
            print("-" * 30)
    
    def cancelar_cita(self, fecha: str, hora: str) -> bool:
        """
        Cancela una cita específica del paciente.
        
        Args:
            fecha: Fecha de la cita a cancelar
            hora: Hora de la cita a cancelar
            
        Returns:
            bool: True si la cita fue cancelada exitosamente, False en caso contrario
        """
        for cita in self._citas:
            if cita.fecha == fecha and cita.hora == hora and cita.estado == "Agendada":
                cita.estado = "Cancelada"
                print(f"Cita cancelada exitosamente para {fecha} a las {hora}")
                return True
        
        print("No se encontró una cita agendada para esa fecha y hora")
        return False
    
    def obtener_citas_agendadas(self) -> List[Cita]:
        """
        Obtiene todas las citas agendadas del paciente.
        
        Returns:
            List[Cita]: Lista de citas agendadas
        """
        return [cita for cita in self._citas if cita.estado == "Agendada"]
    
    def obtener_info_especifica(self) -> str:
        """
        Obtiene información específica del paciente.
        
        Returns:
            str: Información específica del paciente
        """
        citas_agendadas: int = len(self.obtener_citas_agendadas())
        return f"Paciente con {citas_agendadas} citas agendadas"
    
    def mostrar_datos(self) -> None:
        """
        Muestra los datos del paciente.
        
        Este método imprime en consola toda la información
        del paciente incluyendo estadísticas de citas.
        """
        print(f"--- {self._tipo.upper()} ---")
        super().mostrar_datos()
        citas_agendadas: int = len(self.obtener_citas_agendadas())
        print(f"Citas agendadas: {citas_agendadas}")
    
    def __str__(self) -> str:
        """
        Retorna una representación en string del paciente.
        
        Returns:
            str: Representación del paciente
        """
        return f"Paciente: {self._nombre}"
    
    def __repr__(self) -> str:
        """
        Retorna una representación técnica del paciente.
        
        Returns:
            str: Representación técnica del paciente
        """
        return f"Paciente(nombre='{self._nombre}')"



