"""
Operaciones CRUD para HistorialMedico
"""

from typing import List, Optional
from uuid import UUID

from entities.historial_medico import HistorialMedico
from sqlalchemy.orm import Session


class HistorialMedicoCRUD:
    """CRUD para gestión de historiales médicos."""

    def __init__(self, db: Session):
        self.db = db

    def crear_historial(
        self,
        numero_historial: str,
        paciente_id: UUID,
        id_usuario_creacion: UUID,
        notas_generales: str = None,
    ) -> HistorialMedico:
        """Crear un nuevo historial médico."""
        historial = HistorialMedico(
            numero_historial=numero_historial,
            paciente_id=paciente_id,
            notas_generales=notas_generales,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(historial)
        self.db.commit()
        self.db.refresh(historial)
        return historial

    def obtener_historiales(
        self, skip: int = 0, limit: int = 100
    ) -> List[HistorialMedico]:
        """Obtener todos los historiales médicos."""
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.activo)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_historial(self, historial_id: UUID) -> Optional[HistorialMedico]:
        """Obtener un historial médico por ID."""
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.id == historial_id)
            .first()
        )

    def obtener_historial_por_numero(
        self, numero_historial: str
    ) -> Optional[HistorialMedico]:
        """Obtener un historial médico por número."""
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.numero_historial == numero_historial)
            .first()
        )

    def obtener_historial_por_paciente(
        self, paciente_id: UUID
    ) -> Optional[HistorialMedico]:
        """Obtener historial médico por paciente."""
        return (
            self.db.query(HistorialMedico)
            .filter(
                HistorialMedico.paciente_id == paciente_id,
                HistorialMedico.activo,
            )
            .first()
        )

    def obtener_historiales_por_estado(self, estado: str) -> List[HistorialMedico]:
        """Obtener historiales médicos por estado."""
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.estado == estado, HistorialMedico.activo)
            .all()
        )

    def buscar_historiales_por_numero(self, numero: str) -> List[HistorialMedico]:
        """Buscar historiales médicos por número (búsqueda parcial)."""
        return (
            self.db.query(HistorialMedico)
            .filter(
                HistorialMedico.numero_historial.ilike(f"%{numero}%"),
                HistorialMedico.activo,
            )
            .all()
        )

    def actualizar_historial(
        self, historial_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[HistorialMedico]:
        """Actualizar un historial médico."""
        historial = self.obtener_historial(historial_id)
        if historial:
            for key, value in kwargs.items():
                if hasattr(historial, key):
                    setattr(historial, key, value)
            historial.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(historial)
        return historial

    def cerrar_historial(
        self, historial_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[HistorialMedico]:
        """Cerrar un historial médico."""
        return self.actualizar_historial(
            historial_id, id_usuario_edicion, estado="cerrado"
        )

    def archivar_historial(
        self, historial_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[HistorialMedico]:
        """Archivar un historial médico."""
        return self.actualizar_historial(
            historial_id, id_usuario_edicion, estado="archivado"
        )

    def eliminar_historial(self, historial_id: UUID) -> bool:
        """Eliminar un historial médico (soft delete)."""
        historial = self.obtener_historial(historial_id)
        if historial:
            historial.activo = False
            self.db.commit()
            return True
        return False
