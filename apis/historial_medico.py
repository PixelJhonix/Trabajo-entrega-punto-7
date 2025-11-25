from typing import List
from uuid import UUID

from crud.historial_medico_crud import HistorialMedicoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
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
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    include_inactive: bool = Query(False, description="Incluir historiales inactivos"),
    db: Session = Depends(get_db)
):
    """Obtener todos los historiales médicos con paginación y opción de incluir inactivos."""
    try:
        historial_crud = HistorialMedicoCRUD(db)
        historiales = historial_crud.obtener_historiales(
            skip=skip, limit=limit, include_inactive=include_inactive
        )
        if not historiales:
            return []
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
            numero_historial=historial_data.numero_historial,
            paciente_id=historial_data.paciente_id,
            id_usuario_creacion=(
                historial_data.id_usuario_creacion
                if historial_data.id_usuario_creacion
                else None
            ),
            notas_generales=historial_data.notas_generales,
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

        historial_existente = historial_crud.obtener_historial(historial_id)
        if not historial_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial médico no encontrado",
            )

        campos_actualizacion = {
            k: v
            for k, v in historial_data.dict(exclude={"id_usuario_edicion"}).items()
            if v is not None
        }

        if not campos_actualizacion and not historial_data.id_usuario_edicion:
            return historial_existente

        historial_actualizado = historial_crud.actualizar_historial(
            historial_id,
            (
                historial_data.id_usuario_edicion
                if historial_data.id_usuario_edicion
                else None
            ),
            **campos_actualizacion,
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


@router.delete(
    "/{historial_id}", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def eliminar_historial(historial_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un historial médico (soft delete)."""
    try:
        historial_crud = HistorialMedicoCRUD(db)

        historial_existente = historial_crud.obtener_historial(historial_id)
        if not historial_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial médico no encontrado",
            )

        eliminado = historial_crud.eliminar_historial(historial_id)
        if eliminado:
            return RespuestaAPI(
                mensaje="Historial médico eliminado exitosamente", success=True
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
