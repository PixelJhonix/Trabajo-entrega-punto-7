from typing import List
from uuid import UUID

from crud.cita_crud import CitaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas import CitaCreate, CitaResponse, CitaUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/citas", tags=["citas"])


@router.get("/", response_model=List[CitaResponse])
async def obtener_citas(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    include_inactive: bool = Query(False, description="Incluir citas inactivas"),
    db: Session = Depends(get_db)
):
    """Obtener todas las citas con paginación y opción de incluir inactivas."""
    try:
        cita_crud = CitaCRUD(db)
        citas = cita_crud.obtener_citas(
            skip=skip, limit=limit, include_inactive=include_inactive
        )
        if not citas:
            return []
        return citas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener citas: {str(e)}",
        )


@router.get("/{cita_id}", response_model=CitaResponse)
async def obtener_cita(cita_id: UUID, db: Session = Depends(get_db)):
    """Obtener una cita por ID."""
    try:
        cita_crud = CitaCRUD(db)
        cita = cita_crud.obtener_cita(cita_id)
        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
            )
        return cita
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cita: {str(e)}",
        )


@router.get("/paciente/{paciente_id}", response_model=List[CitaResponse])
async def obtener_citas_por_paciente(paciente_id: UUID, db: Session = Depends(get_db)):
    """Obtener citas por paciente."""
    try:
        cita_crud = CitaCRUD(db)
        citas = cita_crud.obtener_citas_por_paciente(paciente_id)
        return citas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener citas por paciente: {str(e)}",
        )


@router.get("/medico/{medico_id}", response_model=List[CitaResponse])
async def obtener_citas_por_medico(medico_id: UUID, db: Session = Depends(get_db)):
    """Obtener citas por médico."""
    try:
        cita_crud = CitaCRUD(db)
        citas = cita_crud.obtener_citas_por_medico(medico_id)
        return citas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener citas por médico: {str(e)}",
        )


@router.get("/fecha/{fecha}", response_model=List[CitaResponse])
async def obtener_citas_por_fecha(fecha: str, db: Session = Depends(get_db)):
    """Obtener citas por fecha."""
    try:
        cita_crud = CitaCRUD(db)
        citas = cita_crud.obtener_citas_por_fecha(fecha)
        return citas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener citas por fecha: {str(e)}",
        )


@router.get("/estado/{estado}", response_model=List[CitaResponse])
async def obtener_citas_por_estado(estado: str, db: Session = Depends(get_db)):
    """Obtener citas por estado."""
    try:
        cita_crud = CitaCRUD(db)
        citas = cita_crud.obtener_citas_por_estado(estado)
        return citas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener citas por estado: {str(e)}",
        )


@router.post("/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
async def crear_cita(cita_data: CitaCreate, db: Session = Depends(get_db)):
    """Crear una nueva cita."""
    try:
        cita_crud = CitaCRUD(db)
        cita = cita_crud.crear_cita(
            paciente_id=cita_data.paciente_id,
            medico_id=cita_data.medico_id,
            fecha_cita=cita_data.fecha_cita,
            motivo=cita_data.motivo,
            id_usuario_creacion=(
                cita_data.id_usuario_creacion if cita_data.id_usuario_creacion else None
            ),
            notas=cita_data.notas,
        )
        return cita
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cita: {str(e)}",
        )


@router.put("/{cita_id}", response_model=CitaResponse)
async def actualizar_cita(
    cita_id: UUID, cita_data: CitaUpdate, db: Session = Depends(get_db)
):
    """Actualizar una cita existente."""
    try:
        cita_crud = CitaCRUD(db)

        cita_existente = cita_crud.obtener_cita(cita_id)
        if not cita_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
            )

        campos_actualizacion = {
            k: v
            for k, v in cita_data.dict(exclude={"id_usuario_edicion"}).items()
            if v is not None
        }

        if not campos_actualizacion and not cita_data.id_usuario_edicion:
            return cita_existente

        cita_actualizada = cita_crud.actualizar_cita(
            cita_id,
            cita_data.id_usuario_edicion if cita_data.id_usuario_edicion else None,
            **campos_actualizacion,
        )
        return cita_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cita: {str(e)}",
        )


@router.patch("/{cita_id}/cancelar", response_model=CitaResponse)
async def cancelar_cita(
    cita_id: UUID, id_usuario_edicion: UUID, db: Session = Depends(get_db)
):
    """Cancelar una cita."""
    try:
        cita_crud = CitaCRUD(db)
        cita = cita_crud.cancelar_cita(cita_id, id_usuario_edicion)
        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
            )
        return cita
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cancelar cita: {str(e)}",
        )


@router.patch("/{cita_id}/completar", response_model=CitaResponse)
async def completar_cita(
    cita_id: UUID, id_usuario_edicion: UUID, db: Session = Depends(get_db)
):
    """Completar una cita."""
    try:
        cita_crud = CitaCRUD(db)
        cita = cita_crud.completar_cita(cita_id, id_usuario_edicion)
        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
            )
        return cita
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al completar cita: {str(e)}",
        )


@router.delete(
    "/{cita_id}", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def eliminar_cita(cita_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una cita (soft delete)."""
    try:
        cita_crud = CitaCRUD(db)

        cita_existente = cita_crud.obtener_cita(cita_id)
        if not cita_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
            )

        eliminada = cita_crud.eliminar_cita(cita_id)
        if eliminada:
            return RespuestaAPI(mensaje="Cita eliminada exitosamente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar cita",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cita: {str(e)}",
        )
