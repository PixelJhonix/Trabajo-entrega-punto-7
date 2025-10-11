"""
API de Factura Detalles - Endpoints para gestión de detalles de factura
"""

from typing import List
from uuid import UUID

from crud.factura_detalle_crud import FacturaDetalleCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    FacturaDetalleCreate,
    FacturaDetalleResponse,
    FacturaDetalleUpdate,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/factura-detalles", tags=["factura-detalles"])


@router.get("/", response_model=List[FacturaDetalleResponse])
async def obtener_detalles(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los detalles de factura con paginación."""
    try:
        detalle_crud = FacturaDetalleCRUD(db)
        detalles = detalle_crud.obtener_detalles(skip=skip, limit=limit)
        return detalles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalles de factura: {str(e)}",
        )


@router.get("/{detalle_id}", response_model=FacturaDetalleResponse)
async def obtener_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    """Obtener un detalle de factura por ID."""
    try:
        detalle_crud = FacturaDetalleCRUD(db)
        detalle = detalle_crud.obtener_detalle(detalle_id)
        if not detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de factura no encontrado",
            )
        return detalle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalle de factura: {str(e)}",
        )


@router.get("/factura/{factura_id}", response_model=List[FacturaDetalleResponse])
async def obtener_detalles_por_factura(factura_id: UUID, db: Session = Depends(get_db)):
    """Obtener detalles por factura."""
    try:
        detalle_crud = FacturaDetalleCRUD(db)
        detalles = detalle_crud.obtener_detalles_por_factura(factura_id)
        return detalles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalles por factura: {str(e)}",
        )


@router.post(
    "/", response_model=FacturaDetalleResponse, status_code=status.HTTP_201_CREATED
)
async def crear_detalle(
    detalle_data: FacturaDetalleCreate, db: Session = Depends(get_db)
):
    """Crear un nuevo detalle de factura."""
    try:
        detalle_crud = FacturaDetalleCRUD(db)
        detalle = detalle_crud.crear_detalle(
            factura_id=detalle_data.factura_id,
            cita_id=detalle_data.cita_id,
            hospitalizacion_id=detalle_data.hospitalizacion_id,
            descripcion=detalle_data.descripcion,
            cantidad=detalle_data.cantidad,
            precio_unitario=detalle_data.precio_unitario,
            subtotal=detalle_data.subtotal,
            id_usuario_creacion=detalle_data.id_usuario_creacion,
        )
        return detalle
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear detalle de factura: {str(e)}",
        )


@router.put("/{detalle_id}", response_model=FacturaDetalleResponse)
async def actualizar_detalle(
    detalle_id: UUID, detalle_data: FacturaDetalleUpdate, db: Session = Depends(get_db)
):
    """Actualizar un detalle de factura existente."""
    try:
        detalle_crud = FacturaDetalleCRUD(db)

        # Verificar que el detalle existe
        detalle_existente = detalle_crud.obtener_detalle(detalle_id)
        if not detalle_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de factura no encontrado",
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in detalle_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return detalle_existente

        detalle_actualizado = detalle_crud.actualizar_detalle(
            detalle_id, detalle_data.id_usuario_edicion, **campos_actualizacion
        )
        return detalle_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar detalle de factura: {str(e)}",
        )


@router.delete("/{detalle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un detalle de factura."""
    try:
        detalle_crud = FacturaDetalleCRUD(db)

        # Verificar que el detalle existe
        detalle_existente = detalle_crud.obtener_detalle(detalle_id)
        if not detalle_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de factura no encontrado",
            )

        eliminado = detalle_crud.eliminar_detalle(detalle_id)
        if eliminado:
            return RespuestaAPI(
                mensaje="Detalle de factura eliminado exitosamente", exito=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar detalle de factura",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar detalle de factura: {str(e)}",
        )
