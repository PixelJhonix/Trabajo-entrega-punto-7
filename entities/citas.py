# Manejo de citas: agendar, ver por paciente/medico/fecha, cancelar.

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .usuario import Usuario
from .profesional import Profesional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class Citas(Base):
    __tablename__ = "citas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    profesional_id = Column(UUID(as_uuid=True), ForeignKey("profesionales.id"))
    fecha = Column(DateTime)

    usuario = relationship("Usuario", back_populates="citas")
    profesional = relationship("Profesional", back_populates="citas")

    def __repr__(self):
        return f"Citas(id={self.id}, usuario_id={self.usuario_id}, profesional_id={self.profesional_id}, fecha='{self.fecha}')"

    @staticmethod
    def ver_citas_paciente(nombre, session):
        usuario = session.query(Usuario).filter(Usuario.nombre == nombre).first()
        if usuario:
            print(f"Citas de {nombre}:")
            for c in usuario.citas:
                print(f"Con {c.profesional.nombre} el {c.fecha.strftime('%Y-%m-%d')}")
        else:
            print("Usuario no encontrado.")

    @staticmethod
    def ver_citas_medico(nombre, session):
        profesional = (
            session.query(Profesional).filter(Profesional.nombre == nombre).first()
        )
        if profesional:
            print(f"Citas de {nombre}:")
            for c in profesional.citas:
                print(f"Con {c.usuario.nombre} el {c.fecha.strftime('%Y-%m-%d')}")
        else:
            print("Profesional no encontrado.")

    @staticmethod
    def ver_citas_fecha(fecha, session):
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        print(f"Citas en {fecha}:")
        for c in session.query(Citas).filter(Citas.fecha == fecha_dt).all():
            print(f"{c.usuario.nombre} con {c.profesional.nombre}")

    @staticmethod
    def cancelar_cita(usuario_nombre, profesional_nombre, fecha, session):
        usuario = (
            session.query(Usuario).filter(Usuario.nombre == usuario_nombre).first()
        )
        profesional = (
            session.query(Profesional)
            .filter(Profesional.nombre == profesional_nombre)
            .first()
        )
        if not usuario or not profesional:
            print("No encontrado.")
            return
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        cita = (
            session.query(Citas)
            .filter(
                Citas.usuario_id == usuario.id,
                Citas.profesional_id == profesional.id,
                Citas.fecha == fecha_dt,
            )
            .first()
        )
        if cita:
            session.delete(cita)
            session.commit()
            print("Cita cancelada.")
        else:
            print("Cita no encontrada.")


class CitasCreate(BaseModel):
    usuario_nombre: str = Field(..., min_length=1)
    profesional_nombre: str = Field(..., min_length=1)
    fecha: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
