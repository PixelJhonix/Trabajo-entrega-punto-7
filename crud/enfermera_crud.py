"""
Operaciones CRUD para Enfermera
"""

from typing import List, Optional
from uuid import UUID

from entities.enfermera import Enfermera
from sqlalchemy.orm import Session


class EnfermeraCRUD:
    """CRUD para gestión de enfermeras."""

    def __init__(self, db: Session):
        self.db = db

    def crear_enfermera(
        self,
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
        numero_licencia: str,
        turno: str,
        id_usuario_creacion: UUID,
    ) -> Enfermera:
        """Crear una nueva enfermera."""
        enfermera = Enfermera(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            numero_licencia=numero_licencia,
            turno=turno,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(enfermera)
        self.db.commit()
        self.db.refresh(enfermera)
        return enfermera

    def obtener_enfermeras(self, skip: int = 0, limit: int = 100) -> List[Enfermera]:
        """Obtener todas las enfermeras."""
        return (
            self.db.query(Enfermera)
            .filter(Enfermera.activo)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_enfermera(self, enfermera_id: UUID) -> Optional[Enfermera]:
        """Obtener una enfermera por ID."""
        return self.db.query(Enfermera).filter(Enfermera.id == enfermera_id).first()

    def obtener_enfermera_por_email(self, email: str) -> Optional[Enfermera]:
        """Obtener una enfermera por email."""
        return self.db.query(Enfermera).filter(Enfermera.email == email).first()

    def obtener_enfermera_por_licencia(
        self, numero_licencia: str
    ) -> Optional[Enfermera]:
        """Obtener una enfermera por número de licencia."""
        return (
            self.db.query(Enfermera)
            .filter(Enfermera.numero_licencia == numero_licencia)
            .first()
        )

    def obtener_enfermeras_por_turno(self, turno: str) -> List[Enfermera]:
        """Obtener enfermeras por turno."""
        return (
            self.db.query(Enfermera)
            .filter(Enfermera.turno == turno, Enfermera.activo)
            .all()
        )

    def buscar_enfermeras_por_nombre(self, nombre: str) -> List[Enfermera]:
        """Buscar enfermeras por nombre."""
        return (
            self.db.query(Enfermera)
            .filter(
                Enfermera.nombre.ilike(f"%{nombre}%"),
                Enfermera.activo,
            )
            .all()
        )

    def actualizar_enfermera(
        self, enfermera_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Enfermera]:
        """Actualizar una enfermera."""
        enfermera = self.obtener_enfermera(enfermera_id)
        if enfermera:
            for key, value in kwargs.items():
                if hasattr(enfermera, key):
                    setattr(enfermera, key, value)
            enfermera.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(enfermera)
        return enfermera

    def eliminar_enfermera(self, enfermera_id: UUID) -> bool:
        """Eliminar una enfermera (soft delete)."""
        enfermera = self.obtener_enfermera(enfermera_id)
        if enfermera:
            enfermera.activo = False
            self.db.commit()
            return True
        return False
