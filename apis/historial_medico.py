"""
API de Historiales Médicos - Endpoints para gestión de historiales médicos
"""

from typing import List
from uuid import UUID

from crud.historial_medico_crud import HistorialMedicoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    HistorialMedicoCreate,
    HistorialMedicoResponse,
    HistorialMedicoUpdate,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/historiales-medicos", tags=["historiales-medicos"])


@router.get("/", response_model=List[HistorialMedicoResponse])
async def obtener_historiales(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los historiales médicos con paginación."""
    try:
        historial_crud = HistorialMedicoCRUD(db)
        historiales = historial_crud.obtener_historiales(skip=skip, limit=limit)
        return historiales
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener historiales médicos: {str(e)}",
        )


@router.get("/{historial_id}", response_model=HistorialMedicoResponse)
async def obtener_historial(historial_id: UUID, db: Session = Depends(get_db)):
    """Obtener un historial médico por ID."""
    try:
        historial_crud = HistorialMedicoCRUD(db)
        historial = historial_crud.obtener_historial(historial_id)
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial médico no encontrado",
            )
        return historial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener historial médico: {str(e)}",
        )


@router.get("/numero/{numero_historial}", response_model=HistorialMedicoResponse)
async def obtener_historial_por_numero(
    numero_historial: str, db: Session = Depends(get_db)
):
    """Obtener un historial médico por número de historial."""
    try:
        historial_crud = HistorialMedicoCRUD(db)
        historial = historial_crud.obtener_historial_por_numero(numero_historial)
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial médico no encontrado",
            )
        return historial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener historial médico: {str(e)}",
        )


@router.get("/paciente/{paciente_id}", response_model=HistorialMedicoResponse)
async def obtener_historial_por_paciente(
    paciente_id: UUID, db: Session = Depends(get_db)
):
    """Obtener historial médico por paciente."""
    try:
        historial_crud = HistorialMedicoCRUD(db)
        historial = historial_crud.obtener_historial_por_paciente(paciente_id)
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial médico no encontrado",
            )
        return historial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener historial médico: {str(e)}",
        )


@router.get("/estado/{estado}", response_model=List[HistorialMedicoResponse])
async def obtener_historiales_por_estado(estado: str, db: Session = Depends(get_db)):
    """Obtener historiales médicos por estado."""
    try:
        historial_crud = HistorialMedicoCRUD(db)
        historiales = historial_crud.obtener_historiales_por_estado(estado)
        return historiales
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener historiales por estado: {str(e)}",
        )


@router.get("/buscar/{numero}", response_model=List[HistorialMedicoResponse])
async def buscar_historiales_por_numero(numero: str, db: Session = Depends(get_db)):
    """Buscar historiales médicos por número (búsqueda parcial)."""
    try:
        historial_crud = HistorialMedicoCRUD(db)
        historiales = historial_crud.buscar_historiales_por_numero(numero)
        return historiales
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar historiales: {str(e)}",
        )


@router.post(
    "/", response_model=HistorialMedicoResponse, status_code=status.HTTP_201_CREATED
)
async def crear_historial(
    historial_data: HistorialMedicoCreate, db: Session = Depends(get_db)
):
    """Crear un nuevo historial médico."""
    try:
        historial_crud = HistorialMedicoCRUD(db)
        historial = historial_crud.crear_historial(
            paciente_id=historial_data.paciente_id,
            numero_historial=historial_data.numero_historial,
            fecha_apertura=historial_data.fecha_apertura,
            id_usuario_creacion=historial_data.id_usuario_creacion,
        )
        return historial
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear historial médico: {str(e)}",
        )


@router.put("/{historial_id}", response_model=HistorialMedicoResponse)
async def actualizar_historial(
    historial_id: UUID,
    historial_data: HistorialMedicoUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un historial médico existente."""
    try:
        historial_crud = HistorialMedicoCRUD(db)

        # Verificar que el historial existe
        historial_existente = historial_crud.obtener_historial(historial_id)
        if not historial_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial médico no encontrado",
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in historial_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return historial_existente

        historial_actualizado = historial_crud.actualizar_historial(
            historial_id, historial_data.id_usuario_edicion, **campos_actualizacion
        )
        return historial_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar historial médico: {str(e)}",
        )


@router.patch("/{historial_id}/cerrar", response_model=HistorialMedicoResponse)
async def cerrar_historial(
    historial_id: UUID, id_usuario_edicion: UUID, db: Session = Depends(get_db)
):
    """Cerrar un historial médico."""
    try:
        historial_crud = HistorialMedicoCRUD(db)
        historial = historial_crud.cerrar_historial(historial_id, id_usuario_edicion)
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial médico no encontrado",
            )
        return historial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cerrar historial médico: {str(e)}",
        )


@router.patch("/{historial_id}/archivar", response_model=HistorialMedicoResponse)
async def archivar_historial(
    historial_id: UUID, id_usuario_edicion: UUID, db: Session = Depends(get_db)
):
    """Archivar un historial médico."""
    try:
        historial_crud = HistorialMedicoCRUD(db)
        historial = historial_crud.archivar_historial(historial_id, id_usuario_edicion)
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial médico no encontrado",
            )
        return historial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al archivar historial médico: {str(e)}",
        )


@router.delete("/{historial_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_historial(historial_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un historial médico."""
    try:
        historial_crud = HistorialMedicoCRUD(db)

        # Verificar que el historial existe
        historial_existente = historial_crud.obtener_historial(historial_id)
        if not historial_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial médico no encontrado",
            )

        eliminado = historial_crud.eliminar_historial(historial_id)
        if eliminado:
            return RespuestaAPI(
                mensaje="Historial médico eliminado exitosamente", exito=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar historial médico",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar historial médico: {str(e)}",
        )
