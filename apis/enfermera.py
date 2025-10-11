"""
API de Enfermeras - Endpoints para gestión de enfermeras
"""

from typing import List
from uuid import UUID

from crud.enfermera_crud import EnfermeraCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import EnfermeraCreate, EnfermeraResponse, EnfermeraUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/enfermeras", tags=["enfermeras"])


@router.get("/", response_model=List[EnfermeraResponse])
async def obtener_enfermeras(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todas las enfermeras con paginación."""
    try:
        enfermera_crud = EnfermeraCRUD(db)
        enfermeras = enfermera_crud.obtener_enfermeras(skip=skip, limit=limit)
        return enfermeras
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener enfermeras: {str(e)}",
        )


@router.get("/{enfermera_id}", response_model=EnfermeraResponse)
async def obtener_enfermera(enfermera_id: UUID, db: Session = Depends(get_db)):
    """Obtener una enfermera por ID."""
    try:
        enfermera_crud = EnfermeraCRUD(db)
        enfermera = enfermera_crud.obtener_enfermera(enfermera_id)
        if not enfermera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Enfermera no encontrada"
            )
        return enfermera
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener enfermera: {str(e)}",
        )


@router.get("/email/{email}", response_model=EnfermeraResponse)
async def obtener_enfermera_por_email(email: str, db: Session = Depends(get_db)):
    """Obtener una enfermera por email."""
    try:
        enfermera_crud = EnfermeraCRUD(db)
        enfermera = enfermera_crud.obtener_enfermera_por_email(email)
        if not enfermera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Enfermera no encontrada"
            )
        return enfermera
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener enfermera: {str(e)}",
        )


@router.get("/licencia/{numero_licencia}", response_model=EnfermeraResponse)
async def obtener_enfermera_por_licencia(
    numero_licencia: str, db: Session = Depends(get_db)
):
    """Obtener una enfermera por número de licencia."""
    try:
        enfermera_crud = EnfermeraCRUD(db)
        enfermera = enfermera_crud.obtener_enfermera_por_licencia(numero_licencia)
        if not enfermera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Enfermera no encontrada"
            )
        return enfermera
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener enfermera: {str(e)}",
        )


@router.get("/turno/{turno}", response_model=List[EnfermeraResponse])
async def obtener_enfermeras_por_turno(turno: str, db: Session = Depends(get_db)):
    """Obtener enfermeras por turno."""
    try:
        enfermera_crud = EnfermeraCRUD(db)
        enfermeras = enfermera_crud.obtener_enfermeras_por_turno(turno)
        return enfermeras
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener enfermeras por turno: {str(e)}",
        )


@router.get("/buscar/{nombre}", response_model=List[EnfermeraResponse])
async def buscar_enfermeras_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """Buscar enfermeras por nombre (búsqueda parcial)."""
    try:
        enfermera_crud = EnfermeraCRUD(db)
        enfermeras = enfermera_crud.buscar_enfermeras_por_nombre(nombre)
        return enfermeras
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar enfermeras: {str(e)}",
        )


@router.post("/", response_model=EnfermeraResponse, status_code=status.HTTP_201_CREATED)
async def crear_enfermera(
    enfermera_data: EnfermeraCreate, db: Session = Depends(get_db)
):
    """Crear una nueva enfermera."""
    try:
        enfermera_crud = EnfermeraCRUD(db)
        enfermera = enfermera_crud.crear_enfermera(
            primer_nombre=enfermera_data.primer_nombre,
            segundo_nombre=enfermera_data.segundo_nombre,
            apellido=enfermera_data.apellido,
            fecha_nacimiento=enfermera_data.fecha_nacimiento,
            especialidad=enfermera_data.especialidad,
            numero_licencia=enfermera_data.numero_licencia,
            turno=enfermera_data.turno,
            telefono=enfermera_data.telefono,
            direccion=enfermera_data.direccion,
            id_usuario_creacion=enfermera_data.id_usuario_creacion,
            email=enfermera_data.email,
        )
        return enfermera
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear enfermera: {str(e)}",
        )


@router.put("/{enfermera_id}", response_model=EnfermeraResponse)
async def actualizar_enfermera(
    enfermera_id: UUID, enfermera_data: EnfermeraUpdate, db: Session = Depends(get_db)
):
    """Actualizar una enfermera existente."""
    try:
        enfermera_crud = EnfermeraCRUD(db)

        # Verificar que la enfermera existe
        enfermera_existente = enfermera_crud.obtener_enfermera(enfermera_id)
        if not enfermera_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Enfermera no encontrada"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in enfermera_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return enfermera_existente

        enfermera_actualizada = enfermera_crud.actualizar_enfermera(
            enfermera_id, enfermera_data.id_usuario_edicion, **campos_actualizacion
        )
        return enfermera_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar enfermera: {str(e)}",
        )


@router.delete("/{enfermera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_enfermera(enfermera_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una enfermera."""
    try:
        enfermera_crud = EnfermeraCRUD(db)

        # Verificar que la enfermera existe
        enfermera_existente = enfermera_crud.obtener_enfermera(enfermera_id)
        if not enfermera_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Enfermera no encontrada"
            )

        eliminada = enfermera_crud.eliminar_enfermera(enfermera_id)
        if eliminada:
            return RespuestaAPI(mensaje="Enfermera eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar enfermera",
            )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar enfermera: {str(e)}",
        )
