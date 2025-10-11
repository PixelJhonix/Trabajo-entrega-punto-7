<<<<<<< Updated upstream
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class Turno(str, Enum):
    manana = "Mañana"
    tarde = "Tarde"
    noche = "Noche"

class PersonaIn(BaseModel):
    nombre: str = Field(min_length=1)
    fecha_nac: str  # Formato dd/mm/yyyy
    telefono: str = Field(pattern=r"^[0-9+\-\s]{7,15}$")
    direccion: str = Field(min_length=3)

    @field_validator("fecha_nac")
    @classmethod
    def validar_fecha(cls, v: str) -> str:
        datetime.strptime(v, "%d/%m/%Y")
        return v

class PacienteIn(PersonaIn):
    pass

class MedicoIn(PersonaIn):
    especialidad: str = Field(min_length=2)

class EnfermeraIn(PersonaIn):
    turno: Turno
=======
"""
Modelos Pydantic para las respuestas de la API
"""

from datetime import date, datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


# Modelos base para Usuario
class UsuarioBase(BaseModel):
    nombre: str
    nombre_usuario: str
    email: EmailStr
    telefono: Optional[str] = None
    es_admin: bool = False


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    nombre_usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    es_admin: Optional[bool] = None
    activo: Optional[bool] = None
    id_usuario_edicion: UUID


class UsuarioResponse(UsuarioBase):
    id: UUID
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contraseña: str


class CambioContraseña(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str


# Modelos base para Paciente
class PacienteBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    apellido: str
    fecha_nacimiento: date
    telefono: str
    email: Optional[str] = None
    direccion: str


class PacienteCreate(PacienteBase):
    id_usuario_creacion: UUID


class PacienteUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class PacienteResponse(PacienteBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos base para Medico
class MedicoBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    apellido: str
    fecha_nacimiento: date
    especialidad: str
    numero_licencia: str
    consultorio: Optional[str] = None
    telefono: str
    email: Optional[str] = None
    direccion: str


class MedicoCreate(MedicoBase):
    id_usuario_creacion: UUID


class MedicoUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    especialidad: Optional[str] = None
    numero_licencia: Optional[str] = None
    consultorio: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class MedicoResponse(MedicoBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos base para Enfermera
class EnfermeraBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    apellido: str
    fecha_nacimiento: date
    especialidad: Optional[str] = None
    numero_licencia: str
    turno: str
    telefono: str
    email: Optional[str] = None
    direccion: str


class EnfermeraCreate(EnfermeraBase):
    id_usuario_creacion: UUID


class EnfermeraUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    especialidad: Optional[str] = None
    numero_licencia: Optional[str] = None
    turno: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class EnfermeraResponse(EnfermeraBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos base para Cita
class CitaBase(BaseModel):
    paciente_id: UUID
    medico_id: UUID
    fecha: date
    hora: time
    motivo: str
    observaciones: Optional[str] = None


class CitaCreate(CitaBase):
    id_usuario_creacion: UUID


class CitaUpdate(BaseModel):
    paciente_id: Optional[UUID] = None
    medico_id: Optional[UUID] = None
    fecha: Optional[date] = None
    hora: Optional[time] = None
    motivo: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class CitaResponse(CitaBase):
    id: UUID
    estado: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos base para Hospitalizacion
class HospitalizacionBase(BaseModel):
    paciente_id: UUID
    medico_responsable_id: UUID
    enfermera_asignada_id: Optional[UUID] = None
    tipo_cuidado: str
    descripcion: str
    numero_habitacion: str
    tipo_habitacion: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None


class HospitalizacionCreate(HospitalizacionBase):
    id_usuario_creacion: UUID


class HospitalizacionUpdate(BaseModel):
    paciente_id: Optional[UUID] = None
    medico_responsable_id: Optional[UUID] = None
    enfermera_asignada_id: Optional[UUID] = None
    tipo_cuidado: Optional[str] = None
    descripcion: Optional[str] = None
    numero_habitacion: Optional[str] = None
    tipo_habitacion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class HospitalizacionResponse(HospitalizacionBase):
    id: UUID
    estado: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos base para Factura
class FacturaBase(BaseModel):
    paciente_id: UUID
    numero_factura: str
    fecha_emision: date
    fecha_limite_pago: date
    total: float
    metodo_pago: Optional[str] = None


class FacturaCreate(FacturaBase):
    id_usuario_creacion: UUID


class FacturaUpdate(BaseModel):
    paciente_id: Optional[UUID] = None
    numero_factura: Optional[str] = None
    fecha_emision: Optional[date] = None
    fecha_limite_pago: Optional[date] = None
    total: Optional[float] = None
    estado: Optional[str] = None
    metodo_pago: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class FacturaResponse(FacturaBase):
    id: UUID
    estado: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos base para FacturaDetalle
class FacturaDetalleBase(BaseModel):
    factura_id: UUID
    cita_id: Optional[UUID] = None
    hospitalizacion_id: Optional[UUID] = None
    descripcion: str
    cantidad: int
    precio_unitario: float
    subtotal: float


class FacturaDetalleCreate(FacturaDetalleBase):
    id_usuario_creacion: UUID


class FacturaDetalleUpdate(BaseModel):
    factura_id: Optional[UUID] = None
    cita_id: Optional[UUID] = None
    hospitalizacion_id: Optional[UUID] = None
    descripcion: Optional[str] = None
    cantidad: Optional[int] = None
    precio_unitario: Optional[float] = None
    subtotal: Optional[float] = None
    id_usuario_edicion: Optional[UUID] = None


class FacturaDetalleResponse(FacturaDetalleBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Modelos base para HistorialMedico
class HistorialMedicoBase(BaseModel):
    paciente_id: UUID
    numero_historial: str
    fecha_apertura: date


class HistorialMedicoCreate(HistorialMedicoBase):
    id_usuario_creacion: UUID


class HistorialMedicoUpdate(BaseModel):
    paciente_id: Optional[UUID] = None
    numero_historial: Optional[str] = None
    fecha_apertura: Optional[date] = None
    estado: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class HistorialMedicoResponse(HistorialMedicoBase):
    id: UUID
    estado: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos base para HistorialEntrada
class HistorialEntradaBase(BaseModel):
    historial_id: UUID
    medico_id: UUID
    cita_id: Optional[UUID] = None
    diagnostico: str
    tratamiento: str
    notas: Optional[str] = None
    fecha_registro: date
    firma_digital: Optional[str] = None


class HistorialEntradaCreate(HistorialEntradaBase):
    id_usuario_creacion: UUID


class HistorialEntradaUpdate(BaseModel):
    historial_id: Optional[UUID] = None
    medico_id: Optional[UUID] = None
    cita_id: Optional[UUID] = None
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    notas: Optional[str] = None
    fecha_registro: Optional[date] = None
    firma_digital: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class HistorialEntradaResponse(HistorialEntradaBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos de respuesta para la API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int
>>>>>>> Stashed changes
