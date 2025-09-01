from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
import re

class Turno(str, Enum):
    """Enum para los turnos de trabajo de las enfermeras"""
    manana = "Mañana"
    tarde = "Tarde"
    noche = "Noche"

class TipoServicio(str, Enum):
    """Enum para los tipos de servicios médicos"""
    consulta = "Consulta"
    procedimiento = "Procedimiento"
    medicamento = "Medicamento"
    examen = "Examen"
    terapia = "Terapia"

class PersonaIn(BaseModel):
    """Esquema base para validar datos de entrada de todas las personas"""
    nombre: str = Field(
        min_length=1, 
        max_length=100,
        pattern=r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\.\-']+$",
        description="Nombre completo de la persona"
    )
    fecha_nac: str = Field(
        pattern=r"^\d{2}/\d{2}/\d{4}$",
        description="Fecha de nacimiento en formato dd/mm/yyyy"
    )
    telefono: str = Field(
        pattern=r"^[0-9+\-\s]{7,15}$",
        description="Número de teléfono"
    )
    direccion: str = Field(
        min_length=3,
        max_length=200,
        description="Dirección de residencia"
    )

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        """
        Valida que el nombre solo contenga caracteres permitidos
        
        Args:
            v: Nombre a validar
            
        Returns:
            str: Nombre validado y limpiado
            
        Raises:
            ValueError: Si el nombre contiene caracteres no permitidos
        """
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\.\-']+$", v):
            raise ValueError("El nombre solo puede contener letras, espacios, puntos, guiones y apóstrofes")
        return v.strip()

    @field_validator("fecha_nac")
    @classmethod
    def validar_fecha_nacimiento(cls, v: str) -> str:
        """
        Valida que la fecha de nacimiento sea válida y no futura
        
        Args:
            v: Fecha a validar
            
        Returns:
            str: Fecha validada
        """
        fecha_obj = datetime.strptime(v, "%d/%m/%Y")
        if fecha_obj > datetime.now():
            raise ValueError("La fecha de nacimiento no puede ser futura")
        return v

class PacienteIn(PersonaIn):
    """Esquema para validar datos de entrada de pacientes"""
    pass

class MedicoIn(PersonaIn):
    """Esquema para validar datos de entrada de médicos"""
    especialidad: str = Field(
        min_length=2,
        max_length=50,
        description="Especialidad médica del doctor"
    )

class EnfermeraIn(PersonaIn):
    """Esquema para validar datos de entrada de enfermeras"""
    turno: Turno = Field(description="Turno de trabajo de la enfermera")

class CitaIn(BaseModel):
    """Esquema para validar datos de entrada de citas médicas"""
    fecha: str = Field(
        pattern=r"^\d{2}/\d{2}/\d{4}$",
        description="Fecha de la cita en formato dd/mm/yyyy"
    )
    hora: str = Field(
        pattern=r"^\d{2}:\d{2}$",
        description="Hora de la cita en formato HH:MM"
    )
    motivo: str = Field(
        min_length=5,
        max_length=200,
        description="Motivo de la consulta"
    )

    @field_validator("fecha")
    @classmethod
    def validar_fecha_cita(cls, v: str) -> str:
        """
        Valida que la fecha de la cita sea futura y válida
        
        Args:
            v: Fecha a validar
            
        Returns:
            str: Fecha validada
        """
        fecha_obj = datetime.strptime(v, "%d/%m/%Y")
        fecha_actual = datetime.now()
        
        if fecha_obj.date() < fecha_actual.date():
            raise ValueError("La fecha de la cita debe ser futura")
            
        return v

    @field_validator("hora")
    @classmethod
    def validar_hora_cita(cls, v: str) -> str:
        """
        Valida que la hora esté en horario laboral
        
        Args:
            v: Hora a validar
            
        Returns:
            str: Hora validada
        """
        hora, minuto = map(int, v.split(':'))
        if not (8 <= hora <= 17) or (hora == 17 and minuto > 0):
            raise ValueError("La hora debe estar entre 8:00 y 17:00")
        return v

class DiagnosticoIn(BaseModel):
    """Esquema para validar datos de entrada de diagnósticos médicos"""
    sintomas: str = Field(
        min_length=10,
        max_length=500,
        description="Descripción detallada de los síntomas"
    )
    diagnostico: str = Field(
        min_length=5,
        max_length=200,
        description="Diagnóstico médico establecido"
    )
    tratamiento: str = Field(
        min_length=10,
        max_length=500,
        description="Tratamiento prescrito para el paciente"
    )
    observaciones: Optional[str] = Field(
        default="",
        max_length=300,
        description="Observaciones adicionales del médico"
    )
    fecha_diagnostico: str = Field(
        pattern=r"^\d{2}/\d{2}/\d{4}$",
        description="Fecha del diagnóstico en formato dd/mm/yyyy"
    )

    @field_validator("fecha_diagnostico")
    @classmethod
    def validar_fecha_diagnostico(cls, v: str) -> str:
        """
        Valida que la fecha del diagnóstico no sea futura
        
        Args:
            v: Fecha a validar
            
        Returns:
            str: Fecha validada
        """
        fecha_obj = datetime.strptime(v, "%d/%m/%Y")
        fecha_actual = datetime.now()
        
        if fecha_obj.date() > fecha_actual.date():
            raise ValueError("La fecha del diagnóstico no puede ser futura")
            
        return v

class FacturaIn(BaseModel):
    """Esquema para validar datos de entrada de facturas"""
    concepto: str = Field(
        min_length=5,
        max_length=100,
        description="Concepto del servicio prestado"
    )
    monto: float = Field(
        gt=0,
        le=1000000,
        description="Monto del servicio (máximo 2 decimales)"
    )
    tipo_servicio: TipoServicio = Field(
        description="Tipo de servicio prestado"
    )
    fecha_servicio: str = Field(
        pattern=r"^\d{2}/\d{2}/\d{4}$",
        description="Fecha del servicio en formato dd/mm/yyyy"
    )
    descripcion: Optional[str] = Field(
        default="",
        max_length=200,
        description="Descripción detallada del servicio"
    )

    @field_validator("fecha_servicio")
    @classmethod
    def validar_fecha_servicio(cls, v: str) -> str:
        """
        Valida que la fecha del servicio sea válida y no futura
        
        Args:
            v: Fecha a validar
            
        Returns:
            str: Fecha validada
        """
        fecha_obj = datetime.strptime(v, "%d/%m/%Y")
        if fecha_obj > datetime.now():
            raise ValueError("La fecha del servicio no puede ser futura")
        return v

    @field_validator("monto")
    @classmethod
    def validar_monto(cls, v: float) -> float:
        """
        Valida que el monto sea positivo y tenga máximo 2 decimales
        
        Args:
            v: Monto a validar
            
        Returns:
            float: Monto validado
        """
        if v <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        if round(v, 2) != v:
            raise ValueError("El monto debe tener máximo 2 decimales")
        return v

# Funciones de validación simplificadas sin try-except
def validar_campo_nombre(nombre: str) -> tuple[bool, str]:
    """Valida el campo nombre usando validación simple"""
    if not nombre or len(nombre.strip()) < 1:
        return False, "El nombre no puede estar vacío"
    
    if len(nombre) > 100:
        return False, "El nombre no puede exceder 100 caracteres"
    
    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\.\-']+$", nombre):
        return False, "El nombre solo puede contener letras, espacios, puntos, guiones y apóstrofes"
    
    return True, ""

def validar_campo_fecha(fecha: str) -> tuple[bool, str]:
    """Valida el campo fecha usando validación simple"""
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", fecha):
        return False, "La fecha debe tener el formato dd/mm/yyyy"
    
    # Validar que sea una fecha válida
    try:
        fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
        if fecha_obj > datetime.now():
            return False, "La fecha de nacimiento no puede ser futura"
        return True, ""
    except ValueError:
        return False, "La fecha ingresada no es válida"

def validar_campo_telefono(telefono: str) -> tuple[bool, str]:
    """Valida el campo teléfono usando validación simple"""
    if not re.match(r"^[0-9+\-\s]{7,15}$", telefono):
        return False, "El teléfono debe tener entre 7 y 15 dígitos"
    
    return True, ""

def validar_campo_direccion(direccion: str) -> tuple[bool, str]:
    """Valida el campo dirección usando validación simple"""
    if not direccion or len(direccion.strip()) < 3:
        return False, "La dirección debe tener al menos 3 caracteres"
    
    if len(direccion) > 200:
        return False, "La dirección no puede exceder 200 caracteres"
    
    return True, ""

def validar_campo_especialidad(especialidad: str) -> tuple[bool, str]:
    """Valida el campo especialidad usando validación simple"""
    if not especialidad or len(especialidad.strip()) < 2:
        return False, "La especialidad debe tener al menos 2 caracteres"
    
    if len(especialidad) > 50:
        return False, "La especialidad no puede exceder 50 caracteres"
    
    return True, ""

def validar_campo_concepto(concepto: str) -> tuple[bool, str]:
    """Valida el campo concepto usando validación simple"""
    if not concepto or len(concepto.strip()) < 5:
        return False, "El concepto debe tener al menos 5 caracteres"
    
    if len(concepto) > 100:
        return False, "El concepto no puede exceder 100 caracteres"
    
    return True, ""

def validar_campo_monto(monto: float) -> tuple[bool, str]:
    """Valida el campo monto usando validación simple"""
    if monto <= 0:
        return False, "El monto debe ser mayor a 0"
    
    if monto > 1000000:
        return False, "El monto no puede exceder $1,000,000"
    
    # Validar decimales
    str_monto = str(monto)
    if '.' in str_monto:
        decimales = len(str_monto.split('.')[1])
        if decimales > 2:
            return False, "El monto debe tener máximo 2 decimales"
    
    return True, ""

def validar_campo_tipo_servicio(tipo_servicio: str) -> tuple[bool, str]:
    """Valida el campo tipo_servicio usando validación simple"""
    tipos_validos = ["Consulta", "Procedimiento", "Medicamento", "Examen", "Terapia"]
    if tipo_servicio not in tipos_validos:
        return False, f"Tipo de servicio debe ser uno de: {', '.join(tipos_validos)}"
    
    return True, ""

def validar_campo_fecha_servicio(fecha_servicio: str) -> tuple[bool, str]:
    """Valida el campo fecha_servicio usando validación simple"""
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", fecha_servicio):
        return False, "La fecha debe tener el formato dd/mm/yyyy"
    
    # Validar que sea una fecha válida
    try:
        fecha_obj = datetime.strptime(fecha_servicio, "%d/%m/%Y")
        if fecha_obj > datetime.now():
            return False, "La fecha del servicio no puede ser futura"
        return True, ""
    except ValueError:
        return False, "La fecha ingresada no es válida"

def validar_campo_descripcion(descripcion: str) -> tuple[bool, str]:
    """Valida el campo descripción usando validación simple"""
    if len(descripcion) > 200:
        return False, "La descripción no puede exceder 200 caracteres"
    
    return True, ""

def validar_campo_motivo(motivo: str) -> tuple[bool, str]:
    """Valida el campo motivo usando validación simple"""
    if not motivo or len(motivo.strip()) < 5:
        return False, "El motivo debe tener al menos 5 caracteres"
    
    if len(motivo) > 200:
        return False, "El motivo no puede exceder 200 caracteres"
    
    return True, ""

def validar_campo_hora(hora: str) -> tuple[bool, str]:
    """Valida el campo hora usando validación simple"""
    if not re.match(r"^\d{2}:\d{2}$", hora):
        return False, "La hora debe tener el formato HH:MM"
    
    try:
        hora_num, minuto_num = map(int, hora.split(':'))
        if not (8 <= hora_num <= 17) or (hora_num == 17 and minuto_num > 0):
            return False, "La hora debe estar entre 8:00 y 17:00"
        return True, ""
    except ValueError:
        return False, "La hora ingresada no es válida"

def validar_campo_sintomas(sintomas: str) -> tuple[bool, str]:
    """Valida el campo síntomas usando validación simple"""
    if not sintomas or len(sintomas.strip()) < 10:
        return False, "Los síntomas deben tener al menos 10 caracteres"
    
    if len(sintomas) > 500:
        return False, "Los síntomas no pueden exceder 500 caracteres"
    
    return True, ""

def validar_campo_diagnostico(diagnostico: str) -> tuple[bool, str]:
    """Valida el campo diagnóstico usando validación simple"""
    if not diagnostico or len(diagnostico.strip()) < 5:
        return False, "El diagnóstico debe tener al menos 5 caracteres"
    
    if len(diagnostico) > 200:
        return False, "El diagnóstico no puede exceder 200 caracteres"
    
    return True, ""

def validar_campo_tratamiento(tratamiento: str) -> tuple[bool, str]:
    """Valida el campo tratamiento usando validación simple"""
    if not tratamiento or len(tratamiento.strip()) < 10:
        return False, "El tratamiento debe tener al menos 10 caracteres"
    
    if len(tratamiento) > 500:
        return False, "El tratamiento no puede exceder 500 caracteres"
    
    return True, ""

def validar_campo_observaciones(observaciones: str) -> tuple[bool, str]:
    """Valida el campo observaciones usando validación simple"""
    if len(observaciones) > 300:
        return False, "Las observaciones no pueden exceder 300 caracteres"
    
    return True, ""
