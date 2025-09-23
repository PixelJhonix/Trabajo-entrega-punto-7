# Manejo de citas: agendar, ver por paciente/medico/fecha, cancelar.

from uuid import UUID
from typing import (
    Any,
)  # esta diciendo que una variable o argumento puede ser de cualquier tipo de dato.


from sqlalchemy import UUID, DateTime, Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .usuario import Usuario
from .profesional import Profesional


class Citas(Base):
    __tablename__ = "citas"
    id = Column(UUID, primary_key=True, index=True)
    usuario_id = Column(UUID, ForeignKey("usuarios.id"))
    profesional_id = Column(UUID, ForeignKey("profesionales.id"))
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
                print(f"Con {c.profesional.nombre} el {c.fecha}")
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
                print(f"Con {c.usuario.nombre} el {c.fecha}")
        else:
            print("Profesional no encontrado.")

    @staticmethod
    def ver_citas_fecha(fecha, session):
        print(f"Citas en {fecha}:")
        for c in session.query(Citas).filter(Citas.fecha == fecha).all():
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
        cita = (
            session.query(Citas)
            .filter(
                Citas.usuario_id == usuario.id,
                Citas.profesional_id == profesional.id,
                Citas.fecha == fecha,
            )
            .first()
        )
        if cita:
            session.delete(cita)
            session.commit()
            print("Cita cancelada.")
        else:
            print("Cita no encontrada.")
