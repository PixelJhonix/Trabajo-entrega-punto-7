"""Módulo para la gestión de citas médicas en el sistema de salud.

Este módulo define el modelo Citas para almacenar los detalles de las citas y el modelo CitasCreate de Pydantic para validar los datos de creación de citas.
También proporciona métodos estáticos para visualizar y cancelar citas.
"""

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
    """Modelo SQLAlchemy que representa una cita médica.

    Atributos:
        id (UUID): Identificador único de la cita.
        usuario_id (UUID): Clave foránea que referencia al usuario.
        profesional_id (UUID): Clave foránea que referencia al profesional.
        fecha (DateTime): Fecha y hora de la cita.
        usuario (Usuario): Relación con el usuario asociado.
        profesional (Profesional): Relación con el profesional asociado.
    """

    __tablename__ = "citas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    profesional_id = Column(UUID(as_uuid=True), ForeignKey("profesionales.id"))
    fecha = Column(DateTime)

    usuario = relationship("Usuario", back_populates="citas")
    profesional = relationship("Profesional", back_populates="citas")

    def __repr__(self):
        """Representación en cadena de la instancia de Citas."""
        return f"Citas(id={self.id}, usuario_id={self.usuario_id}, profesional_id={self.profesional_id}, fecha='{self.fecha}')"

    @staticmethod
    def ver_citas_paciente(nombre, session):
        """Muestra todas las citas de un paciente específico.

        Args:
            nombre (str): Nombre del paciente.
            session (Session): Sesión de SQLAlchemy para consultas a la base de datos.
        """
        usuario = session.query(Usuario).filter(Usuario.nombre == nombre).first()
        if usuario:
            print(f"Citas de {nombre}:")
            for c in usuario.citas:
                print(f"Con {c.profesional.nombre} el {c.fecha.strftime('%Y-%m-%d')}")
        else:
            print("Usuario no encontrado.")

    @staticmethod
    def ver_citas_medico(nombre, session):
        """Muestra todas las citas de un profesional médico específico.

        Args:
            nombre (str): Nombre del profesional.
            session (Session): Sesión de SQLAlchemy para consultas a la base de datos.
        """
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
        """Muestra todas las citas para una fecha específica.

        Args:
            fecha (str): Fecha en formato 'YYYY-MM-DD'.
            session (Session): Sesión de SQLAlchemy para consultas a la base de datos.
        """
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        print(f"Citas en {fecha}:")
        for c in session.query(Citas).filter(Citas.fecha == fecha_dt).all():
            print(f"{c.usuario.nombre} con {c.profesional.nombre}")

    @staticmethod
    def cancelar_cita(usuario_nombre, profesional_nombre, fecha, session):
        """Cancela una cita según usuario, profesional y fecha.

        Args:
            usuario_nombre (str): Nombre del usuario.
            profesional_nombre (str): Nombre del profesional.
            fecha (str): Fecha de la cita en formato 'YYYY-MM-DD'.
            session (Session): Sesión de SQLAlchemy para consultas a la base de datos.
        """
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
    """Modelo Pydantic para validar los datos de creación de citas.

    Atributos:
        usuario_nombre (str): Nombre del usuario.
        profesional_nombre (str): Nombre del profesional.
        fecha (str): Fecha de la cita en formato 'YYYY-MM-DD'.
    """

    usuario_nombre: str = Field(..., min_length=1)
    profesional_nombre: str = Field(..., min_length=1)
    fecha: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
