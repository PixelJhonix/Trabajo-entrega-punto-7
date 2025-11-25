import re
from typing import List, Optional
from uuid import UUID

from entities.medico import Medico
from sqlalchemy.orm import Session


class MedicoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def _validar_email(self, email: str) -> bool:
        """Validar formato de email."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def _validar_telefono(self, telefono: str) -> bool:
        """Validar formato de teléfono."""
        if not telefono:
            return True
        pattern = r"^[0-9+\-\s()]+$"
        return bool(re.match(pattern, telefono)) and len(telefono) <= 20

    def crear_medico(
        self,
        nombre: str,
        apellido: str,
        email: str,
        especialidad: str,
        numero_licencia: str,
        fecha_nacimiento,
        id_usuario_creacion: Optional[UUID] = None,
        telefono: Optional[str] = None,
        consultorio: Optional[str] = None,
        direccion: Optional[str] = None,
    ) -> Medico:
        """Crear un nuevo médico."""
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre es obligatorio")
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if not apellido or len(apellido.strip()) == 0:
            raise ValueError("El apellido es obligatorio")
        if len(apellido) > 100:
            raise ValueError("El apellido no puede exceder 100 caracteres")

        if not fecha_nacimiento:
            raise ValueError("La fecha de nacimiento es obligatoria")

        if not especialidad or len(especialidad.strip()) == 0:
            raise ValueError("La especialidad es obligatoria")
        if len(especialidad) > 100:
            raise ValueError("La especialidad no puede exceder 100 caracteres")

        if not numero_licencia or len(numero_licencia.strip()) == 0:
            raise ValueError("El número de licencia es obligatorio")
        if len(numero_licencia) > 50:
            raise ValueError("El número de licencia no puede exceder 50 caracteres")

        if self.obtener_medico_por_licencia(numero_licencia):
            raise ValueError("El número de licencia ya está registrado")

        if telefono and not self._validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        if direccion and len(direccion.strip()) < 3:
            raise ValueError("La dirección debe tener al menos 3 caracteres")
        if direccion and len(direccion) > 255:
            raise ValueError("La dirección no puede exceder 255 caracteres")

        if not email or not self._validar_email(email):
            raise ValueError("Email inválido")

        if self.obtener_medico_por_email(email):
            raise ValueError("El email ya está registrado")

        medico = Medico(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            fecha_nacimiento=fecha_nacimiento,
            especialidad=especialidad.strip(),
            numero_licencia=numero_licencia.strip(),
            consultorio=consultorio.strip() if consultorio else None,
            telefono=telefono.strip() if telefono else None,
            email=email.lower().strip(),
            direccion=direccion.strip() if direccion else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(medico)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def obtener_medicos(
        self, 
        skip: int = 0, 
        limit: int = 1000, 
        include_inactive: bool = False,
        nombre: Optional[str] = None,
        especialidad: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> List[Medico]:
        """Obtener todos los médicos con opción de incluir inactivos y filtros de búsqueda."""
        try:
            query = self.db.query(Medico)
            if not include_inactive:
                query = query.filter(Medico.activo == True)
            
            if activo is not None:
                query = query.filter(Medico.activo == activo)
            
            if nombre:
                query = query.filter(
                    (Medico.nombre.ilike(f"%{nombre}%")) | 
                    (Medico.apellido.ilike(f"%{nombre}%"))
                )
            
            if especialidad:
                query = query.filter(Medico.especialidad.ilike(f"%{especialidad}%"))
            
            medicos = query.offset(skip).limit(limit).all()
            return medicos if medicos else []
        except Exception as e:
            self.db.rollback()
            import logging

            logging.error(f"Error al obtener médicos: {str(e)}")
            raise ValueError(f"Error al obtener médicos: {str(e)}")

    def obtener_medico(self, medico_id: UUID) -> Optional[Medico]:
        """Obtener un médico por ID."""
        return self.db.query(Medico).filter(Medico.id == medico_id).first()

    def obtener_medico_por_email(self, email: str) -> Optional[Medico]:
        """Obtener un médico por email."""
        return self.db.query(Medico).filter(Medico.email == email.lower()).first()

    def obtener_medico_por_licencia(self, numero_licencia: str) -> Optional[Medico]:
        """Obtener un médico por número de licencia."""
        return (
            self.db.query(Medico)
            .filter(Medico.numero_licencia == numero_licencia)
            .first()
        )

    def obtener_medicos_por_especialidad(self, especialidad: str) -> List[Medico]:
        """Obtener médicos por especialidad."""
        return (
            self.db.query(Medico)
            .filter(Medico.especialidad == especialidad, Medico.activo)
            .all()
        )

    def buscar_medicos_por_nombre(self, nombre: str) -> List[Medico]:
        """Buscar médicos por nombre."""
        return (
            self.db.query(Medico)
            .filter(
                Medico.nombre.ilike(f"%{nombre}%"),
                Medico.activo == True,
            )
            .all()
        )

    def actualizar_medico(
        self, medico_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Medico]:
        """Actualizar un médico."""
        medico = self.obtener_medico(medico_id)
        if not medico:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "apellido" in kwargs:
            apellido = kwargs["apellido"]
            if not apellido or len(apellido.strip()) == 0:
                raise ValueError("El apellido es obligatorio")
            if len(apellido) > 100:
                raise ValueError("El apellido no puede exceder 100 caracteres")
            kwargs["apellido"] = apellido.strip()

        if "especialidad" in kwargs:
            especialidad = kwargs["especialidad"]
            if not especialidad or len(especialidad.strip()) == 0:
                raise ValueError("La especialidad es obligatoria")
            if len(especialidad) > 100:
                raise ValueError("La especialidad no puede exceder 100 caracteres")
            kwargs["especialidad"] = especialidad.strip()

        if "numero_licencia" in kwargs:
            licencia = kwargs["numero_licencia"]
            if not licencia or len(licencia.strip()) == 0:
                raise ValueError("El número de licencia es obligatorio")
            if len(licencia) > 50:
                raise ValueError("El número de licencia no puede exceder 50 caracteres")
            if (
                self.obtener_medico_por_licencia(licencia)
                and self.obtener_medico_por_licencia(licencia).id != medico_id
            ):
                raise ValueError("El número de licencia ya está registrado")
            kwargs["numero_licencia"] = licencia.strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            telefono = kwargs["telefono"]
            if not self._validar_telefono(telefono):
                raise ValueError("Formato de teléfono inválido")
            kwargs["telefono"] = telefono.strip()

        if "direccion" in kwargs and kwargs["direccion"]:
            direccion = kwargs["direccion"]
            if len(direccion.strip()) < 3:
                raise ValueError("La dirección debe tener al menos 3 caracteres")
            if len(direccion) > 255:
                raise ValueError("La dirección no puede exceder 255 caracteres")
            kwargs["direccion"] = direccion.strip()

        if "email" in kwargs and kwargs["email"]:
            email = kwargs["email"]
            if not self._validar_email(email):
                raise ValueError("Email inválido")
            if (
                self.obtener_medico_por_email(email)
                and self.obtener_medico_por_email(email).id != medico_id
            ):
                raise ValueError("El email ya está registrado")
            kwargs["email"] = email.lower().strip()

        if id_usuario_edicion:
            medico.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(medico, key):
                setattr(medico, key, value)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def inactivar_medico(self, medico_id: UUID) -> bool:
        """Inactivar un médico (soft delete)."""
        medico = self.obtener_medico(medico_id)
        if not medico:
            return False
        if not medico.activo:
            return True
        medico.activo = False
        self.db.commit()
        return True

    def reactivar_medico(self, medico_id: UUID) -> bool:
        """Reactivar un médico inactivo."""
        medico = self.obtener_medico(medico_id)
        if not medico:
            return False
        if medico.activo:
            return True
        medico.activo = True
        self.db.commit()
        return True

    def eliminar_medico_permanente(self, medico_id: UUID) -> bool:
        """Eliminar un médico permanentemente de la base de datos."""
        import logging
        from sqlalchemy import text
        try:
            medico = self.obtener_medico(medico_id)
            if not medico:
                raise ValueError(f"Médico con ID {medico_id} no encontrado")

            # Actualizar referencias de id_usuario_creacion e id_usuario_edicion
            tablas_usuario = ['tbl_medicos', 'tbl_pacientes', 'tbl_enfermeras', 'tbl_citas', 
                             'tbl_hospitalizaciones', 'tbl_facturas', 'tbl_historiales_medicos', 
                             'tbl_historiales_entradas', 'tbl_facturas_detalles']
            
            for tabla in tablas_usuario:
                try:
                    self.db.execute(
                        text(f"UPDATE {tabla} SET id_usuario_creacion = NULL WHERE id_usuario_creacion = :medico_id"),
                        {"medico_id": str(medico_id)}
                    )
                    self.db.execute(
                        text(f"UPDATE {tabla} SET id_usuario_edicion = NULL WHERE id_usuario_edicion = :medico_id"),
                        {"medico_id": str(medico_id)}
                    )
                except Exception as e:
                    logging.warning(f"Error al actualizar referencias de usuario en {tabla}: {str(e)}")
                    continue

            # Eliminar o inactivar registros relacionados que tienen ForeignKey NOT NULL
            # Citas: eliminar permanentemente las citas del médico
            from entities.cita import Cita
            citas = self.db.query(Cita).filter(Cita.medico_id == medico_id).all()
            for cita in citas:
                self.db.delete(cita)

            # Hospitalizaciones: eliminar permanentemente las hospitalizaciones del médico
            from entities.hospitalizacion import Hospitalizacion
            hospitalizaciones = self.db.query(Hospitalizacion).filter(Hospitalizacion.medico_id == medico_id).all()
            for hosp in hospitalizaciones:
                self.db.delete(hosp)

            # Historiales Entrada: eliminar permanentemente los historiales del médico
            from entities.historial_entrada import HistorialEntrada
            historiales = self.db.query(HistorialEntrada).filter(HistorialEntrada.medico_id == medico_id).all()
            for hist in historiales:
                self.db.delete(hist)

            # Commit de las eliminaciones relacionadas
            self.db.commit()

            # Eliminar el médico
            self.db.delete(medico)
            self.db.commit()
            
            logging.info(f"Médico {medico_id} eliminado permanentemente")
            return True
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error al eliminar médico permanentemente {medico_id}: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            raise ValueError(f"Error al eliminar médico: {str(e)}")

    def eliminar_medico(self, medico_id: UUID) -> bool:
        """Eliminar un médico (soft delete) - mantiene compatibilidad."""
        return self.inactivar_medico(medico_id)
