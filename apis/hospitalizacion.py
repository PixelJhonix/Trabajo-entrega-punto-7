"""
API de Hospitalizaciones - Endpoints para gestión de hospitalizaciones
"""

from typing import List
from uuid import UUID

from crud.hospitalizacion_crud import HospitalizacionCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    HospitalizacionCreate,
    HospitalizacionResponse,
    HospitalizacionUpdate,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/hospitalizaciones", tags=["hospitalizaciones"])


@router.get("/", response_model=List[HospitalizacionResponse])
async def obtener_hospitalizaciones(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todas las hospitalizaciones con paginación."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)
        hospitalizaciones = hospitalizacion_crud.obtener_hospitalizaciones(
            skip=skip, limit=limit
        )
        return hospitalizaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener hospitalizaciones: {str(e)}",
        )


@router.get("/{hospitalizacion_id}", response_model=HospitalizacionResponse)
async def obtener_hospitalizacion(
    hospitalizacion_id: UUID, db: Session = Depends(get_db)
):
    """Obtener una hospitalización por ID."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)
        hospitalizacion = hospitalizacion_crud.obtener_hospitalizacion(
            hospitalizacion_id
        )
        if not hospitalizacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hospitalización no encontrada",
            )
        return hospitalizacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener hospitalización: {str(e)}",
        )


@router.get("/paciente/{paciente_id}", response_model=List[HospitalizacionResponse])
async def obtener_hospitalizaciones_por_paciente(
    paciente_id: UUID, db: Session = Depends(get_db)
):
    """Obtener hospitalizaciones por paciente."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)
        hospitalizaciones = hospitalizacion_crud.obtener_hospitalizaciones_por_paciente(
            paciente_id
        )
        return hospitalizaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener hospitalizaciones por paciente: {str(e)}",
        )


@router.get("/medico/{medico_id}", response_model=List[HospitalizacionResponse])
async def obtener_hospitalizaciones_por_medico(
    medico_id: UUID, db: Session = Depends(get_db)
):
    """Obtener hospitalizaciones por médico responsable."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)
        hospitalizaciones = hospitalizacion_crud.obtener_hospitalizaciones_por_medico(
            medico_id
        )
        return hospitalizaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener hospitalizaciones por médico: {str(e)}",
        )


@router.get("/estado/{estado}", response_model=List[HospitalizacionResponse])
async def obtener_hospitalizaciones_por_estado(
    estado: str, db: Session = Depends(get_db)
):
    """Obtener hospitalizaciones por estado."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)
        hospitalizaciones = hospitalizacion_crud.obtener_hospitalizaciones_por_estado(
            estado
        )
        return hospitalizaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener hospitalizaciones por estado: {str(e)}",
        )


@router.get(
    "/habitacion/{numero_habitacion}", response_model=List[HospitalizacionResponse]
)
async def obtener_hospitalizaciones_por_habitacion(
    numero_habitacion: str, db: Session = Depends(get_db)
):
    """Obtener hospitalizaciones por número de habitación."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)
        hospitalizaciones = (
            hospitalizacion_crud.obtener_hospitalizaciones_por_habitacion(
                numero_habitacion
            )
        )
        return hospitalizaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener hospitalizaciones por habitación: {str(e)}",
        )


@router.post(
    "/", response_model=HospitalizacionResponse, status_code=status.HTTP_201_CREATED
)
async def crear_hospitalizacion(
    hospitalizacion_data: HospitalizacionCreate, db: Session = Depends(get_db)
):
    """Crear una nueva hospitalización."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)
        hospitalizacion = hospitalizacion_crud.crear_hospitalizacion(
            paciente_id=hospitalizacion_data.paciente_id,
            medico_responsable_id=hospitalizacion_data.medico_responsable_id,
            enfermera_asignada_id=hospitalizacion_data.enfermera_asignada_id,
            tipo_cuidado=hospitalizacion_data.tipo_cuidado,
            descripcion=hospitalizacion_data.descripcion,
            numero_habitacion=hospitalizacion_data.numero_habitacion,
            tipo_habitacion=hospitalizacion_data.tipo_habitacion,
            fecha_inicio=hospitalizacion_data.fecha_inicio,
            fecha_fin=hospitalizacion_data.fecha_fin,
            id_usuario_creacion=hospitalizacion_data.id_usuario_creacion,
        )
        return hospitalizacion
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear hospitalización: {str(e)}",
        )


@router.put("/{hospitalizacion_id}", response_model=HospitalizacionResponse)
async def actualizar_hospitalizacion(
    hospitalizacion_id: UUID,
    hospitalizacion_data: HospitalizacionUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar una hospitalización existente."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)

        hospitalizacion_existente = hospitalizacion_crud.obtener_hospitalizacion(
            hospitalizacion_id
        )
        if not hospitalizacion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hospitalización no encontrada",
            )

        campos_actualizacion = {
            k: v for k, v in hospitalizacion_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return hospitalizacion_existente

        hospitalizacion_actualizada = hospitalizacion_crud.actualizar_hospitalizacion(
            hospitalizacion_id,
            hospitalizacion_data.id_usuario_edicion,
            **campos_actualizacion,
        )
        return hospitalizacion_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar hospitalización: {str(e)}",
        )


@router.patch("/{hospitalizacion_id}/completar", response_model=HospitalizacionResponse)
async def completar_hospitalizacion(
    hospitalizacion_id: UUID, id_usuario_edicion: UUID, db: Session = Depends(get_db)
):
    """Completar una hospitalización."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)
        hospitalizacion = hospitalizacion_crud.completar_hospitalizacion(
            hospitalizacion_id, id_usuario_edicion
        )
        if not hospitalizacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hospitalización no encontrada",
            )
        return hospitalizacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al completar hospitalización: {str(e)}",
        )


@router.patch("/{hospitalizacion_id}/cancelar", response_model=HospitalizacionResponse)
async def cancelar_hospitalizacion(
    hospitalizacion_id: UUID, id_usuario_edicion: UUID, db: Session = Depends(get_db)
):
    """Cancelar una hospitalización."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)
        hospitalizacion = hospitalizacion_crud.cancelar_hospitalizacion(
            hospitalizacion_id, id_usuario_edicion
        )
        if not hospitalizacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hospitalización no encontrada",
            )
        return hospitalizacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cancelar hospitalización: {str(e)}",
        )


@router.delete("/{hospitalizacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_hospitalizacion(
    hospitalizacion_id: UUID, db: Session = Depends(get_db)
):
    """Eliminar una hospitalización."""
    try:
        hospitalizacion_crud = HospitalizacionCRUD(db)

        hospitalizacion_existente = hospitalizacion_crud.obtener_hospitalizacion(
            hospitalizacion_id
        )
        if not hospitalizacion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hospitalización no encontrada",
            )

        eliminada = hospitalizacion_crud.eliminar_hospitalizacion(hospitalizacion_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Hospitalización eliminada exitosamente", exito=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar hospitalización",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar hospitalización: {str(e)}",
        )
