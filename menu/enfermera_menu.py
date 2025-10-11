"""Menú interactivo para gestión de enfermeras."""

import os
from uuid import UUID

from auth.auth_service import AuthService
from crud.enfermera_crud import EnfermeraCRUD
from sqlalchemy.orm import Session


class EnfermeraMenu:
    """Menú para gestión de enfermeras."""

    def __init__(self, db: Session, auth_service: AuthService):
        self.db = db
        self.auth_service = auth_service
        self.enfermera_crud = EnfermeraCRUD(db)

    def limpiar_pantalla(self):
        """Limpiar la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_titulo(self):
        """Mostrar título del menú."""
        print("GESTIÓN DE ENFERMERAS")
        print("-" * 25)

    def mostrar_menu(self):
        """Mostrar menú principal de enfermeras."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                print("1. Registrar Enfermera")
                print("2. Buscar Enfermera")
                print("3. Listar Enfermeras")
                print("4. Actualizar Enfermera")
                print("5. Eliminar Enfermera")
                print("0. Volver al Menú Principal")

                opcion = input("\n-> Seleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.registrar_enfermera()
                elif opcion == "2":
                    self.buscar_enfermera()
                elif opcion == "3":
                    self.listar_enfermeras()
                elif opcion == "4":
                    self.actualizar_enfermera()
                elif opcion == "5":
                    self.eliminar_enfermera()
                else:
                    print("Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                print("\n\nRegresando al menú principal...")
                break
            except Exception as e:
                print(f"Error: {e}")
                input("Presione Enter para continuar...")

    def registrar_enfermera(self):
        """Registrar una nueva enfermera."""
        try:
            self.limpiar_pantalla()
            print("REGISTRAR ENFERMERA")
            print("-" * 20)

            primer_nombre = input("Primer nombre: ").strip()
            segundo_nombre = input("Segundo nombre (opcional): ").strip() or None
            apellido = input("Apellido: ").strip()
            fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
            especialidad = input("Especialidad (opcional): ").strip() or None
            numero_licencia = input("Número de licencia: ").strip()
            turno = input("Turno (Mañana/Tarde/Noche): ").strip()
            telefono = input("Teléfono: ").strip()
            email = input("Email (opcional): ").strip() or None
            direccion = input("Dirección: ").strip()

            enfermera = self.enfermera_crud.crear_enfermera(
                primer_nombre=primer_nombre,
                segundo_nombre=segundo_nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                especialidad=especialidad,
                numero_licencia=numero_licencia,
                turno=turno,
                telefono=telefono,
                email=email,
                direccion=direccion,
                id_usuario_creacion=self.auth_service.get_current_user().id,
            )

            print("\nEnfermera registrada exitosamente!")
            print(f"ID: {enfermera.id}")
            print(f"Nombre: {enfermera.primer_nombre} {enfermera.apellido}")
            print(f"Especialidad: {enfermera.especialidad}")
            print(f"Turno: {enfermera.turno}")

        except ValueError as e:
            print(f"Error de validación: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def buscar_enfermera(self):
        """Buscar una enfermera."""
        try:
            self.limpiar_pantalla()
            print("DIAGNOSTICO BUSCAR ENFERMERA")
            print("-" * 25)

            print("1. DIAGNOSTICO Por ID")
            print("2. EMAIL Por Email")
            print("3. USUARIO Por Nombre")
            print("4. HORA Por Turno")

            opcion = input("\n-> Seleccione tipo de búsqueda: ").strip()

            if opcion == "1":
                enfermera_id = input("Ingrese ID de la enfermera: ").strip()
                try:
                    enfermera = self.enfermera_crud.obtener_enfermera(
                        UUID(enfermera_id)
                    )
                    if enfermera:
                        self.mostrar_enfermera(enfermera)
                    else:
                        print("ERROR Enfermera no encontrada")
                except ValueError:
                    print("ERROR ID inválido")

            elif opcion == "2":
                email = input("EMAIL Ingrese email: ").strip()
                enfermera = self.enfermera_crud.obtener_enfermera_por_email(email)
                if enfermera:
                    self.mostrar_enfermera(enfermera)
                else:
                    print("ERROR Enfermera no encontrada")

            elif opcion == "3":
                nombre = input("USUARIO Ingrese nombre a buscar: ").strip()
                enfermeras = self.enfermera_crud.buscar_enfermeras_por_nombre(nombre)
                if enfermeras:
                    print(f"\nLICENCIA Encontradas {len(enfermeras)} enfermera(s):")
                    for enfermera in enfermeras:
                        self.mostrar_enfermera_resumen(enfermera)
                else:
                    print("ERROR No se encontraron enfermeras")

            elif opcion == "4":
                turno = input("HORA Ingrese turno (Mañana/Tarde/Noche): ").strip()
                enfermeras = self.enfermera_crud.buscar_enfermeras_por_turno(turno)
                if enfermeras:
                    print(f"\nLICENCIA Encontradas {len(enfermeras)} enfermera(s):")
                    for enfermera in enfermeras:
                        self.mostrar_enfermera_resumen(enfermera)
                else:
                    print("ERROR No se encontraron enfermeras")

            else:
                print("ERROR Opción inválida")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def listar_enfermeras(self):
        """Listar todas las enfermeras."""
        try:
            self.limpiar_pantalla()
            print("LICENCIA LISTAR ENFERMERAS")
            print("-" * 25)

            enfermeras = self.enfermera_crud.obtener_enfermeras()
            if enfermeras:
                print(f"\nLICENCIA Total de enfermeras: {len(enfermeras)}")
                for enfermera in enfermeras:
                    self.mostrar_enfermera_resumen(enfermera)
            else:
                print("ERROR No hay enfermeras registradas")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def actualizar_enfermera(self):
        """Actualizar una enfermera."""
        try:
            self.limpiar_pantalla()
            print("EDITAR ACTUALIZAR ENFERMERA")
            print("-" * 30)

            enfermera_id = input("Ingrese ID de la enfermera: ").strip()
            enfermera = self.enfermera_crud.obtener_enfermera(UUID(enfermera_id))
            if not enfermera:
                print("ERROR Enfermera no encontrada")
                return

            print("\nLICENCIA Enfermera actual:")
            self.mostrar_enfermera(enfermera)

            print(
                "\nEDITAR Ingrese nuevos datos (deje en blanco para mantener el actual):"
            )

            primer_nombre = input(
                f"USUARIO Primer nombre [{enfermera.primer_nombre}]: "
            ).strip()
            segundo_nombre = input(
                f"USUARIO Segundo nombre [{enfermera.segundo_nombre or 'N/A'}]: "
            ).strip()
            apellido = input(f"USUARIO Apellido [{enfermera.apellido}]: ").strip()
            especialidad = input(
                f"SISTEMA Especialidad [{enfermera.especialidad or 'N/A'}]: "
            ).strip()
            numero_licencia = input(
                f"LICENCIA Número de licencia [{enfermera.numero_licencia}]: "
            ).strip()
            turno = input(f"HORA Turno [{enfermera.turno}]: ").strip()
            telefono = input(f"TELEFONO Teléfono [{enfermera.telefono}]: ").strip()
            email = input(f"EMAIL Email [{enfermera.email or 'N/A'}]: ").strip()
            direccion = input(f"DIRECCION Dirección [{enfermera.direccion}]: ").strip()

            kwargs = {}
            if primer_nombre:
                kwargs["primer_nombre"] = primer_nombre
            if segundo_nombre:
                kwargs["segundo_nombre"] = segundo_nombre
            if apellido:
                kwargs["apellido"] = apellido
            if especialidad:
                kwargs["especialidad"] = especialidad
            if numero_licencia:
                kwargs["numero_licencia"] = numero_licencia
            if turno:
                kwargs["turno"] = turno
            if telefono:
                kwargs["telefono"] = telefono
            if email:
                kwargs["email"] = email
            if direccion:
                kwargs["direccion"] = direccion

            if kwargs:
                enfermera_actualizada = self.enfermera_crud.actualizar_enfermera(
                    enfermera.id, self.auth_service.get_current_user().id, **kwargs
                )
                print("\nOK Enfermera actualizada exitosamente!")
                self.mostrar_enfermera(enfermera_actualizada)
            else:
                print("ℹ No se realizaron cambios")

        except ValueError as e:
            print(f"Error de validación: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def eliminar_enfermera(self):
        """Eliminar una enfermera."""
        try:
            self.limpiar_pantalla()
            print("ELIMINAR ELIMINAR ENFERMERA")
            print("-" * 25)

            enfermera_id = input("Ingrese ID de la enfermera: ").strip()
            enfermera = self.enfermera_crud.obtener_enfermera(UUID(enfermera_id))
            if not enfermera:
                print("ERROR Enfermera no encontrada")
                return

            print("\nLICENCIA Enfermera a eliminar:")
            self.mostrar_enfermera(enfermera)

            confirmacion = (
                input("\nADVERTENCIA ¿Está seguro de eliminar esta enfermera? (s/N): ")
                .strip()
                .lower()
            )
            if confirmacion == "s":
                if self.enfermera_crud.eliminar_enfermera(enfermera.id):
                    print("OK Enfermera eliminada exitosamente!")
                else:
                    print("ERROR Error al eliminar la enfermera")
            else:
                print("ℹOperación cancelada")

        except ValueError as e:
            print(f"Error de validación: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def mostrar_enfermera(self, enfermera):
        """Mostrar información completa de una enfermera."""
        print("\nENFERMERA INFORMACIÓN DE LA ENFERMERA")
        print("-" * 35)
        print(f"ID ID: {enfermera.id}")
        print(
            f"USUARIO Nombre: {enfermera.primer_nombre} {enfermera.segundo_nombre or ''} {enfermera.apellido}"
        )
        print(f"FECHA Fecha de nacimiento: {enfermera.fecha_nacimiento}")
        print(f"SISTEMA Especialidad: {enfermera.especialidad or 'N/A'}")
        print(f"LICENCIA Número de licencia: {enfermera.numero_licencia}")
        print(f"HORA Turno: {enfermera.turno}")
        print(f"TELEFONO Teléfono: {enfermera.telefono}")
        print(f"EMAIL Email: {enfermera.email or 'N/A'}")
        print(f"DIRECCION Dirección: {enfermera.direccion}")
        print(f"FECHA Creado: {enfermera.created_at}")

    def mostrar_enfermera_resumen(self, enfermera):
        """Mostrar resumen de una enfermera."""
        print(
            f"ID {enfermera.id} | USUARIO {enfermera.primer_nombre} {enfermera.apellido} | HORA {enfermera.turno} | TELEFONO {enfermera.telefono}"
        )
