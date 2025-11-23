from typing import List
from uuid import UUID

from crud.factura_crud import FacturaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas import FacturaCreate, FacturaResponse, FacturaUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/facturas", tags=["facturas"])


@router.get("/", response_model=List[FacturaResponse])
async def obtener_facturas(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    include_inactive: bool = Query(False, description="Incluir facturas inactivas"),
    db: Session = Depends(get_db)
):
    """Obtener todas las facturas con paginación y opción de incluir inactivas."""
    try:
        factura_crud = FacturaCRUD(db)
        facturas = factura_crud.obtener_facturas(
            skip=skip, limit=limit, include_inactive=include_inactive
        )
        if not facturas:
            return []
        return facturas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener facturas: {str(e)}",
        )


@router.get("/{factura_id}", response_model=FacturaResponse)
async def obtener_factura(factura_id: UUID, db: Session = Depends(get_db)):
    """Obtener una factura por ID."""
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.obtener_factura(factura_id)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )
        return factura
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener factura: {str(e)}",
        )


@router.get("/numero/{numero_factura}", response_model=FacturaResponse)
async def obtener_factura_por_numero(
    numero_factura: str, db: Session = Depends(get_db)
):
    """Obtener una factura por número de factura."""
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.obtener_factura_por_numero(numero_factura)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )
        return factura
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener factura: {str(e)}",
        )


@router.get("/paciente/{paciente_id}", response_model=List[FacturaResponse])
async def obtener_facturas_por_paciente(
    paciente_id: UUID, db: Session = Depends(get_db)
):
    """Obtener facturas por paciente."""
    try:
        factura_crud = FacturaCRUD(db)
        facturas = factura_crud.obtener_facturas_por_paciente(paciente_id)
        return facturas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener facturas por paciente: {str(e)}",
        )


@router.get("/estado/{estado}", response_model=List[FacturaResponse])
async def obtener_facturas_por_estado(estado: str, db: Session = Depends(get_db)):
    """Obtener facturas por estado."""
    try:
        factura_crud = FacturaCRUD(db)
        facturas = factura_crud.obtener_facturas_por_estado(estado)
        return facturas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener facturas por estado: {str(e)}",
        )


@router.get("/fecha/{fecha}", response_model=List[FacturaResponse])
async def obtener_facturas_por_fecha(fecha: str, db: Session = Depends(get_db)):
    """Obtener facturas por fecha de emisión."""
    try:
        factura_crud = FacturaCRUD(db)
        facturas = factura_crud.obtener_facturas_por_fecha(fecha)
        return facturas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener facturas por fecha: {str(e)}",
        )


@router.get("/vencidas/lista", response_model=List[FacturaResponse])
async def obtener_facturas_vencidas(db: Session = Depends(get_db)):
    """Obtener facturas vencidas."""
    try:
        factura_crud = FacturaCRUD(db)
        facturas = factura_crud.obtener_facturas_vencidas()
        return facturas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener facturas vencidas: {str(e)}",
        )


@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
async def crear_factura(factura_data: FacturaCreate, db: Session = Depends(get_db)):
    """Crear una nueva factura."""
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.crear_factura(
            numero_factura=factura_data.numero_factura,
            fecha_emision=factura_data.fecha_emision,
            fecha_vencimiento=factura_data.fecha_vencimiento,
            subtotal=factura_data.subtotal,
            total=factura_data.total,
            paciente_id=factura_data.paciente_id,
            id_usuario_creacion=(
                factura_data.id_usuario_creacion
                if factura_data.id_usuario_creacion
                else None
            ),
            impuestos=factura_data.impuestos,
            notas=factura_data.notas,
        )
        return factura
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear factura: {str(e)}",
        )


@router.put("/{factura_id}", response_model=FacturaResponse)
async def actualizar_factura(
    factura_id: UUID, factura_data: FacturaUpdate, db: Session = Depends(get_db)
):
    """Actualizar una factura existente."""
    try:
        factura_crud = FacturaCRUD(db)

        factura_existente = factura_crud.obtener_factura(factura_id)
        if not factura_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )

        campos_actualizacion = {
            k: v
            for k, v in factura_data.dict(exclude={"id_usuario_edicion"}).items()
            if v is not None
        }

        if not campos_actualizacion and not factura_data.id_usuario_edicion:
            return factura_existente

        factura_actualizada = factura_crud.actualizar_factura(
            factura_id,
            (
                factura_data.id_usuario_edicion
                if factura_data.id_usuario_edicion
                else None
            ),
            **campos_actualizacion,
        )
        return factura_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar factura: {str(e)}",
        )


@router.patch("/{factura_id}/pagar", response_model=FacturaResponse)
async def pagar_factura(
    factura_id: UUID,
    id_usuario_edicion: UUID,
    db: Session = Depends(get_db),
):
    """Marcar una factura como pagada."""
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.pagar_factura(factura_id, id_usuario_edicion)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )
        return factura
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al pagar factura: {str(e)}",
        )


@router.patch("/{factura_id}/cancelar", response_model=FacturaResponse)
async def cancelar_factura(
    factura_id: UUID, id_usuario_edicion: UUID, db: Session = Depends(get_db)
):
    """Cancelar una factura."""
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.cancelar_factura(factura_id, id_usuario_edicion)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )
        return factura
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cancelar factura: {str(e)}",
        )


@router.post("/marcar-vencidas", response_model=RespuestaAPI)
async def marcar_facturas_vencidas(db: Session = Depends(get_db)):
    """Marcar facturas vencidas automáticamente."""
    try:
        factura_crud = FacturaCRUD(db)
        facturas_vencidas = factura_crud.obtener_facturas_vencidas()
        cantidad = 0
        for factura in facturas_vencidas:
            factura_crud.marcar_vencida(
                factura.id, factura.id_usuario_edicion or factura.id_usuario_creacion
            )
            cantidad += 1
        return RespuestaAPI(
            mensaje=f"Se marcaron {cantidad} facturas como vencidas",
            success=True,
            datos={"facturas_marcadas": cantidad},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al marcar facturas vencidas: {str(e)}",
        )


@router.delete(
    "/{factura_id}", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def eliminar_factura(factura_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una factura (soft delete)."""
    try:
        factura_crud = FacturaCRUD(db)

        factura_existente = factura_crud.obtener_factura(factura_id)
        if not factura_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )

        eliminada = factura_crud.eliminar_factura(factura_id)
        if eliminada:
            return RespuestaAPI(mensaje="Factura eliminada exitosamente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar factura",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar factura: {str(e)}",
        )
