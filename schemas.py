"""
Modelos Pydantic para las respuestas de la API
"""

from datetime import date, datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


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


class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    fecha_nacimiento: date
    direccion: Optional[str] = None


class PacienteCreate(PacienteBase):
    id_usuario_creacion: UUID


class PacienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    activo: Optional[bool] = None
    id_usuario_edicion: Optional[UUID] = None


class PacienteResponse(PacienteBase):
    id: UUID
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MedicoBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    especialidad: str
    numero_licencia: str


class MedicoCreate(MedicoBase):
    id_usuario_creacion: UUID


class MedicoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    especialidad: Optional[str] = None
    numero_licencia: Optional[str] = None
    activo: Optional[bool] = None
    id_usuario_edicion: Optional[UUID] = None


class MedicoResponse(MedicoBase):
    id: UUID
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EnfermeraBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    numero_licencia: str
    turno: str


class EnfermeraCreate(EnfermeraBase):
    id_usuario_creacion: UUID


class EnfermeraUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    numero_licencia: Optional[str] = None
    turno: Optional[str] = None
    activo: Optional[bool] = None
    id_usuario_edicion: Optional[UUID] = None


class EnfermeraResponse(EnfermeraBase):
    id: UUID
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CitaBase(BaseModel):
    fecha_cita: datetime
    motivo: str
    notas: Optional[str] = None
    paciente_id: UUID
    medico_id: UUID


class CitaCreate(CitaBase):
    id_usuario_creacion: UUID


class CitaUpdate(BaseModel):
    fecha_cita: Optional[datetime] = None
    motivo: Optional[str] = None
    notas: Optional[str] = None
    estado: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class CitaResponse(CitaBase):
    id: UUID
    estado: str
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HospitalizacionBase(BaseModel):
    fecha_ingreso: datetime
    fecha_salida: Optional[datetime] = None
    motivo: str
    numero_habitacion: str
    notas: Optional[str] = None
    paciente_id: UUID
    medico_id: UUID
    enfermera_id: Optional[UUID] = None


class HospitalizacionCreate(HospitalizacionBase):
    id_usuario_creacion: UUID


class HospitalizacionUpdate(BaseModel):
    fecha_ingreso: Optional[datetime] = None
    fecha_salida: Optional[datetime] = None
    motivo: Optional[str] = None
    numero_habitacion: Optional[str] = None
    notas: Optional[str] = None
    estado: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class HospitalizacionResponse(HospitalizacionBase):
    id: UUID
    estado: str
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HistorialMedicoBase(BaseModel):
    numero_historial: str
    notas_generales: Optional[str] = None
    paciente_id: UUID


class HistorialMedicoCreate(HistorialMedicoBase):
    id_usuario_creacion: UUID


class HistorialMedicoUpdate(BaseModel):
    numero_historial: Optional[str] = None
    notas_generales: Optional[str] = None
    estado: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class HistorialMedicoResponse(HistorialMedicoBase):
    id: UUID
    estado: str
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HistorialEntradaBase(BaseModel):
    fecha_consulta: datetime
    diagnostico: str
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    historial_medico_id: UUID
    medico_id: UUID


class HistorialEntradaCreate(HistorialEntradaBase):
    id_usuario_creacion: UUID


class HistorialEntradaUpdate(BaseModel):
    fecha_consulta: Optional[datetime] = None
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class HistorialEntradaResponse(HistorialEntradaBase):
    id: UUID
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FacturaBase(BaseModel):
    numero_factura: str
    fecha_emision: datetime
    fecha_vencimiento: datetime
    subtotal: float
    impuestos: float = 0
    total: float
    notas: Optional[str] = None
    paciente_id: UUID


class FacturaCreate(FacturaBase):
    id_usuario_creacion: UUID


class FacturaUpdate(BaseModel):
    numero_factura: Optional[str] = None
    fecha_emision: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
    subtotal: Optional[float] = None
    impuestos: Optional[float] = None
    total: Optional[float] = None
    notas: Optional[str] = None
    estado: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class FacturaResponse(FacturaBase):
    id: UUID
    estado: str
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FacturaDetalleBase(BaseModel):
    descripcion: str
    cantidad: float
    precio_unitario: float
    subtotal: float
    factura_id: UUID


class FacturaDetalleCreate(FacturaDetalleBase):
    id_usuario_creacion: UUID


class FacturaDetalleUpdate(BaseModel):
    descripcion: Optional[str] = None
    cantidad: Optional[float] = None
    precio_unitario: Optional[float] = None
    subtotal: Optional[float] = None
    id_usuario_edicion: Optional[UUID] = None


class FacturaDetalleResponse(FacturaDetalleBase):
    id: UUID
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    success: bool = True


class RespuestaError(BaseModel):
    error_type: str
    message: str
    success: bool = False
    details: Optional[dict] = None
