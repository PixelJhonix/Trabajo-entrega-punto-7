"""
Operaciones CRUD para HistorialEntrada
"""

from typing import List, Optional
from uuid import UUID

from entities.historial_entrada import HistorialEntrada
from sqlalchemy.orm import Session


class HistorialEntradaCRUD:
    """CRUD para gestión de entradas del historial médico."""

    def __init__(self, db: Session):
        self.db = db

    def crear_entrada(
        self,
        fecha_consulta,
        diagnostico: str,
        historial_medico_id: UUID,
        medico_id: UUID,
        id_usuario_creacion: UUID,
        tratamiento: str = None,
        observaciones: str = None,
    ) -> HistorialEntrada:
        """Crear una nueva entrada del historial."""
        entrada = HistorialEntrada(
            fecha_consulta=fecha_consulta,
            diagnostico=diagnostico,
            historial_medico_id=historial_medico_id,
            medico_id=medico_id,
            tratamiento=tratamiento,
            observaciones=observaciones,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(entrada)
        self.db.commit()
        self.db.refresh(entrada)
        return entrada

    def obtener_entradas(
        self, skip: int = 0, limit: int = 100
    ) -> List[HistorialEntrada]:
        """Obtener todas las entradas del historial."""
        return (
            self.db.query(HistorialEntrada)
            .filter(HistorialEntrada.activo)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_entrada(self, entrada_id: UUID) -> Optional[HistorialEntrada]:
        """Obtener una entrada del historial por ID."""
        return (
            self.db.query(HistorialEntrada)
            .filter(HistorialEntrada.id == entrada_id)
            .first()
        )

    def obtener_entradas_por_historial(
        self, historial_id: UUID
    ) -> List[HistorialEntrada]:
        """Obtener entradas por historial médico."""
        return (
            self.db.query(HistorialEntrada)
            .filter(
                HistorialEntrada.historial_medico_id == historial_id,
                HistorialEntrada.activo,
            )
            .all()
        )

    def obtener_entradas_por_medico(self, medico_id: UUID) -> List[HistorialEntrada]:
        """Obtener entradas por médico."""
        return (
            self.db.query(HistorialEntrada)
            .filter(HistorialEntrada.medico_id == medico_id, HistorialEntrada.activo)
            .all()
        )

    def buscar_entradas_por_diagnostico(
        self, diagnostico: str
    ) -> List[HistorialEntrada]:
        """Buscar entradas por diagnóstico."""
        return (
            self.db.query(HistorialEntrada)
            .filter(
                HistorialEntrada.diagnostico.ilike(f"%{diagnostico}%"),
                HistorialEntrada.activo,
            )
            .all()
        )

    def actualizar_entrada(
        self, entrada_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[HistorialEntrada]:
        """Actualizar una entrada del historial."""
        entrada = self.obtener_entrada(entrada_id)
        if entrada:
            for key, value in kwargs.items():
                if hasattr(entrada, key):
                    setattr(entrada, key, value)
            entrada.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(entrada)
        return entrada

    def eliminar_entrada(self, entrada_id: UUID) -> bool:
        """Eliminar una entrada del historial (soft delete)."""
        entrada = self.obtener_entrada(entrada_id)
        if entrada:
            entrada.activo = False
            self.db.commit()
            return True
        return False
