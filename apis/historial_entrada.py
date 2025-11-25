from typing import List
from uuid import UUID

from crud.historial_entrada_crud import HistorialEntradaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas import (
    HistorialEntradaCreate,
    HistorialEntradaResponse,
    HistorialEntradaUpdate,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/historial-entradas", tags=["historial-entradas"])


@router.get("/", response_model=List[HistorialEntradaResponse])
async def obtener_entradas(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    include_inactive: bool = Query(False, description="Incluir entradas inactivas"),
    db: Session = Depends(get_db)
):
    """Obtener todas las entradas del historial con paginación y opción de incluir inactivas."""
    try:
        entrada_crud = HistorialEntradaCRUD(db)
        entradas = entrada_crud.obtener_entradas(
            skip=skip, limit=limit, include_inactive=include_inactive
        )
        if not entradas:
            return []
        return entradas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener entradas del historial: {str(e)}",
        )


@router.get("/{entrada_id}", response_model=HistorialEntradaResponse)
async def obtener_entrada(entrada_id: UUID, db: Session = Depends(get_db)):
    """Obtener una entrada del historial por ID."""
    try:
        entrada_crud = HistorialEntradaCRUD(db)
        entrada = entrada_crud.obtener_entrada(entrada_id)
        if not entrada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entrada del historial no encontrada",
            )
        return entrada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener entrada del historial: {str(e)}",
        )


@router.get("/historial/{historial_id}", response_model=List[HistorialEntradaResponse])
async def obtener_entradas_por_historial(
    historial_id: UUID, db: Session = Depends(get_db)
):
    """Obtener entradas por historial médico."""
    try:
        entrada_crud = HistorialEntradaCRUD(db)
        entradas = entrada_crud.obtener_entradas_por_historial(historial_id)
        return entradas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener entradas por historial: {str(e)}",
        )


@router.get("/medico/{medico_id}", response_model=List[HistorialEntradaResponse])
async def obtener_entradas_por_medico(medico_id: UUID, db: Session = Depends(get_db)):
    """Obtener entradas por médico."""
    try:
        entrada_crud = HistorialEntradaCRUD(db)
        entradas = entrada_crud.obtener_entradas_por_medico(medico_id)
        return entradas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener entradas por médico: {str(e)}",
        )


@router.get("/buscar/{diagnostico}", response_model=List[HistorialEntradaResponse])
async def buscar_entradas_por_diagnostico(
    diagnostico: str, db: Session = Depends(get_db)
):
    """Buscar entradas por diagnóstico (búsqueda parcial)."""
    try:
        entrada_crud = HistorialEntradaCRUD(db)
        entradas = entrada_crud.buscar_entradas_por_diagnostico(diagnostico)
        return entradas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar entradas por diagnóstico: {str(e)}",
        )


@router.post(
    "/", response_model=HistorialEntradaResponse, status_code=status.HTTP_201_CREATED
)
async def crear_entrada(
    entrada_data: HistorialEntradaCreate, db: Session = Depends(get_db)
):
    """Crear una nueva entrada del historial."""
    try:
        entrada_crud = HistorialEntradaCRUD(db)
        entrada = entrada_crud.crear_entrada(
            fecha_consulta=entrada_data.fecha_consulta,
            diagnostico=entrada_data.diagnostico,
            historial_medico_id=entrada_data.historial_medico_id,
            medico_id=entrada_data.medico_id,
            id_usuario_creacion=(
                entrada_data.id_usuario_creacion
                if entrada_data.id_usuario_creacion
                else None
            ),
            tratamiento=entrada_data.tratamiento,
            observaciones=entrada_data.observaciones,
        )
        return entrada
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear entrada del historial: {str(e)}",
        )


@router.put("/{entrada_id}", response_model=HistorialEntradaResponse)
async def actualizar_entrada(
    entrada_id: UUID,
    entrada_data: HistorialEntradaUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar una entrada del historial existente."""
    try:
        entrada_crud = HistorialEntradaCRUD(db)

        entrada_existente = entrada_crud.obtener_entrada(entrada_id)
        if not entrada_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entrada del historial no encontrada",
            )

        campos_actualizacion = {
            k: v
            for k, v in entrada_data.dict(exclude={"id_usuario_edicion"}).items()
            if v is not None
        }

        if not campos_actualizacion and not entrada_data.id_usuario_edicion:
            return entrada_existente

        entrada_actualizada = entrada_crud.actualizar_entrada(
            entrada_id,
            (
                entrada_data.id_usuario_edicion
                if entrada_data.id_usuario_edicion
                else None
            ),
            **campos_actualizacion,
        )
        return entrada_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar entrada del historial: {str(e)}",
        )


@router.delete(
    "/{entrada_id}", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def eliminar_entrada(entrada_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una entrada del historial (soft delete)."""
    try:
        entrada_crud = HistorialEntradaCRUD(db)

        entrada_existente = entrada_crud.obtener_entrada(entrada_id)
        if not entrada_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entrada del historial no encontrada",
            )

        eliminada = entrada_crud.eliminar_entrada(entrada_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Entrada del historial eliminada exitosamente", success=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar entrada del historial",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar entrada del historial: {str(e)}",
        )
