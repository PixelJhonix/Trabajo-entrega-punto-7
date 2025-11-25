from typing import List
from uuid import UUID

from crud.paciente_crud import PacienteCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas import PacienteCreate, PacienteResponse, PacienteUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/pacientes", tags=["pacientes"])


@router.get("/", response_model=List[PacienteResponse])
async def obtener_pacientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    include_inactive: bool = Query(False, description="Incluir pacientes inactivos"),
    nombre: str = Query(None, description="Filtrar por nombre (búsqueda parcial)"),
    activo: bool = Query(None, description="Filtrar por estado activo/inactivo"),
    db: Session = Depends(get_db)
):
    """Obtener todos los pacientes con paginación, opción de incluir inactivos y filtros de búsqueda."""
    try:
        paciente_crud = PacienteCRUD(db)
        pacientes = paciente_crud.obtener_pacientes(
            skip=skip, 
            limit=limit, 
            include_inactive=include_inactive,
            nombre=nombre,
            activo=activo
        )
        if not pacientes:
            return []
        return pacientes
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        import traceback

        error_detail = f"Error al obtener pacientes: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail,
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
            nombre=paciente_data.nombre,
            apellido=paciente_data.apellido,
            email=paciente_data.email,
            fecha_nacimiento=paciente_data.fecha_nacimiento,
            telefono=paciente_data.telefono,
            direccion=paciente_data.direccion,
            id_usuario_creacion=(
                paciente_data.id_usuario_creacion
                if paciente_data.id_usuario_creacion
                else None
            ),
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

        paciente_existente = paciente_crud.obtener_paciente(paciente_id)
        if not paciente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
            )

        campos_actualizacion = {
            k: v
            for k, v in paciente_data.dict(exclude={"id_usuario_edicion"}).items()
            if v is not None
        }

        if not campos_actualizacion and not paciente_data.id_usuario_edicion:
            return paciente_existente

        paciente_actualizado = paciente_crud.actualizar_paciente(
            paciente_id,
            (
                paciente_data.id_usuario_edicion
                if paciente_data.id_usuario_edicion
                else None
            ),
            **campos_actualizacion,
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


@router.patch(
    "/{paciente_id}/inactivar", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def inactivar_paciente(paciente_id: UUID, db: Session = Depends(get_db)):
    """Inactivar un paciente (soft delete)."""
    try:
        paciente_crud = PacienteCRUD(db)
        paciente_existente = paciente_crud.obtener_paciente(paciente_id)
        if not paciente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
            )
        inactivado = paciente_crud.inactivar_paciente(paciente_id)
        if inactivado:
            return RespuestaAPI(mensaje="Paciente inactivado exitosamente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al inactivar paciente",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al inactivar paciente: {str(e)}",
        )


@router.patch(
    "/{paciente_id}/reactivar", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def reactivar_paciente(paciente_id: UUID, db: Session = Depends(get_db)):
    """Reactivar un paciente inactivo."""
    try:
        paciente_crud = PacienteCRUD(db)
        paciente_existente = paciente_crud.obtener_paciente(paciente_id)
        if not paciente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
            )
        reactivado = paciente_crud.reactivar_paciente(paciente_id)
        if reactivado:
            return RespuestaAPI(mensaje="Paciente reactivado exitosamente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al reactivar paciente",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reactivar paciente: {str(e)}",
        )


@router.delete(
    "/{paciente_id}", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def eliminar_paciente_permanente(paciente_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un paciente permanentemente de la base de datos."""
    try:
        paciente_crud = PacienteCRUD(db)
        paciente_existente = paciente_crud.obtener_paciente(paciente_id)
        if not paciente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
            )
        eliminado = paciente_crud.eliminar_paciente_permanente(paciente_id)
        if eliminado:
            return RespuestaAPI(mensaje="Paciente eliminado permanentemente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar paciente",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar paciente: {str(e)}",
        )
