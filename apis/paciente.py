"""
API de Pacientes - Endpoints para gestión de pacientes
"""

from typing import List
from uuid import UUID

from crud.paciente_crud import PacienteCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import PacienteCreate, PacienteResponse, PacienteUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/pacientes", tags=["pacientes"])


@router.get("/", response_model=List[PacienteResponse])
async def obtener_pacientes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los pacientes con paginación."""
    try:
        paciente_crud = PacienteCRUD(db)
        pacientes = paciente_crud.obtener_pacientes(skip=skip, limit=limit)
        return pacientes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener pacientes: {str(e)}",
        )


@router.get("/{paciente_id}", response_model=PacienteResponse)
async def obtener_paciente(paciente_id: UUID, db: Session = Depends(get_db)):
    """Obtener un paciente por ID."""
    try:
        paciente_crud = PacienteCRUD(db)
        paciente = paciente_crud.obtener_paciente(paciente_id)
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
            )
        return paciente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener paciente: {str(e)}",
        )


@router.get("/email/{email}", response_model=PacienteResponse)
async def obtener_paciente_por_email(email: str, db: Session = Depends(get_db)):
    """Obtener un paciente por email."""
    try:
        paciente_crud = PacienteCRUD(db)
        paciente = paciente_crud.obtener_paciente_por_email(email)
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
            )
        return paciente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener paciente: {str(e)}",
        )


@router.get("/buscar/{nombre}", response_model=List[PacienteResponse])
async def buscar_pacientes_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """Buscar pacientes por nombre (búsqueda parcial)."""
    try:
        paciente_crud = PacienteCRUD(db)
        pacientes = paciente_crud.buscar_pacientes_por_nombre(nombre)
        return pacientes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar pacientes: {str(e)}",
        )


@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_paciente(paciente_data: PacienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo paciente."""
    try:
        paciente_crud = PacienteCRUD(db)
        paciente = paciente_crud.crear_paciente(
            primer_nombre=paciente_data.primer_nombre,
            segundo_nombre=paciente_data.segundo_nombre,
            apellido=paciente_data.apellido,
            fecha_nacimiento=paciente_data.fecha_nacimiento,
            telefono=paciente_data.telefono,
            direccion=paciente_data.direccion,
            id_usuario_creacion=paciente_data.id_usuario_creacion,
            email=paciente_data.email,
        )
        return paciente
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear paciente: {str(e)}",
        )


@router.put("/{paciente_id}", response_model=PacienteResponse)
async def actualizar_paciente(
    paciente_id: UUID, paciente_data: PacienteUpdate, db: Session = Depends(get_db)
):
    """Actualizar un paciente existente."""
    try:
        paciente_crud = PacienteCRUD(db)

        # Verificar que el paciente existe
        paciente_existente = paciente_crud.obtener_paciente(paciente_id)
        if not paciente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in paciente_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return paciente_existente

        paciente_actualizado = paciente_crud.actualizar_paciente(
            paciente_id, paciente_data.id_usuario_edicion, **campos_actualizacion
        )
        return paciente_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar paciente: {str(e)}",
        )


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_paciente(paciente_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un paciente."""
    try:
        paciente_crud = PacienteCRUD(db)

        # Verificar que el paciente existe
        paciente_existente = paciente_crud.obtener_paciente(paciente_id)
        if not paciente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
            )

        eliminado = paciente_crud.eliminar_paciente(paciente_id)
        if eliminado:
            return RespuestaAPI(mensaje="Paciente eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar paciente",
            )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar paciente: {str(e)}",
        )
