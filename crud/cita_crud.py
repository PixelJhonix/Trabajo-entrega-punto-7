"""
Operaciones CRUD para Cita
"""

from typing import List, Optional
from uuid import UUID

from entities.cita import Cita
from sqlalchemy.orm import Session


class CitaCRUD:
    """CRUD para gestión de citas."""

    def __init__(self, db: Session):
        self.db = db

    def crear_cita(
        self,
        fecha_cita,
        motivo: str,
        paciente_id: UUID,
        medico_id: UUID,
        id_usuario_creacion: UUID,
        notas: str = None,
    ) -> Cita:
        """Crear una nueva cita."""
        cita = Cita(
            fecha_cita=fecha_cita,
            motivo=motivo,
            paciente_id=paciente_id,
            medico_id=medico_id,
            notas=notas,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(cita)
        self.db.commit()
        self.db.refresh(cita)
        return cita

    def obtener_citas(self, skip: int = 0, limit: int = 100) -> List[Cita]:
        """Obtener todas las citas."""
        return self.db.query(Cita).filter(Cita.activo).offset(skip).limit(limit).all()

    def obtener_cita(self, cita_id: UUID) -> Optional[Cita]:
        """Obtener una cita por ID."""
        return self.db.query(Cita).filter(Cita.id == cita_id).first()

    def obtener_citas_por_paciente(self, paciente_id: UUID) -> List[Cita]:
        """Obtener citas por paciente."""
        return (
            self.db.query(Cita)
            .filter(Cita.paciente_id == paciente_id, Cita.activo)
            .all()
        )

    def obtener_citas_por_medico(self, medico_id: UUID) -> List[Cita]:
        """Obtener citas por médico."""
        return (
            self.db.query(Cita).filter(Cita.medico_id == medico_id, Cita.activo).all()
        )

    def obtener_citas_por_fecha(self, fecha) -> List[Cita]:
        """Obtener citas por fecha."""
        return (
            self.db.query(Cita)
            .filter(Cita.fecha_cita.date() == fecha, Cita.activo)
            .all()
        )

    def obtener_citas_por_estado(self, estado: str) -> List[Cita]:
        """Obtener citas por estado."""
        return self.db.query(Cita).filter(Cita.estado == estado, Cita.activo).all()

    def actualizar_cita(
        self, cita_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Cita]:
        """Actualizar una cita."""
        cita = self.obtener_cita(cita_id)
        if cita:
            for key, value in kwargs.items():
                if hasattr(cita, key):
                    setattr(cita, key, value)
            cita.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(cita)
        return cita

    def cancelar_cita(self, cita_id: UUID, id_usuario_edicion: UUID) -> Optional[Cita]:
        """Cancelar una cita."""
        return self.actualizar_cita(cita_id, id_usuario_edicion, estado="cancelada")

    def completar_cita(self, cita_id: UUID, id_usuario_edicion: UUID) -> Optional[Cita]:
        """Completar una cita."""
        return self.actualizar_cita(cita_id, id_usuario_edicion, estado="completada")

    def eliminar_cita(self, cita_id: UUID) -> bool:
        """Eliminar una cita (soft delete)."""
        cita = self.obtener_cita(cita_id)
        if cita:
            cita.activo = False
            self.db.commit()
            return True
        return False
