"""Menú interactivo para gestión de usuarios."""

import os
from uuid import UUID
from sqlalchemy.orm import Session
from crud.usuario_crud import UsuarioCRUD
from auth.auth_service import AuthService


class UsuarioMenu:
    """Menú para gestión de usuarios (solo administradores)."""

    def __init__(self, db: Session, auth_service: AuthService):
        self.db = db
        self.auth_service = auth_service
        self.usuario_crud = UsuarioCRUD(db)

    def limpiar_pantalla(self):
        """Limpiar la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_titulo(self):
        """Mostrar título del menú."""
        print("GESTION GESTIÓN DE USUARIOS")
        print("-" * 30)

    def mostrar_menu(self):
        """Mostrar menú principal de usuarios."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                print("1. + Crear Usuario")
                print("2. DIAGNOSTICO Buscar Usuario")
                print("3. LICENCIA Listar Usuarios")
                print("4. EDITAR Actualizar Usuario")
                print("5. ELIMINAR Eliminar Usuario")
                print("6. CAMBIAR Cambiar Estado Usuario")
                print("0. VOLVER Volver al Menú Principal")

                opcion = input("\n-> Seleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.crear_usuario()
                elif opcion == "2":
                    self.buscar_usuario()
                elif opcion == "3":
                    self.listar_usuarios()
                elif opcion == "4":
                    self.actualizar_usuario()
                elif opcion == "5":
                    self.eliminar_usuario()
                elif opcion == "6":
                    self.cambiar_estado_usuario()
                else:
                    print("ERROR Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                print("\n\nADIOS Regresando al menú principal...")
                break
            except Exception as e:
                print(f"ERROR Error: {e}")
                input("Presione Enter para continuar...")

    def crear_usuario(self):
        """Crear un nuevo usuario."""
        try:
            self.limpiar_pantalla()
            print("GESTION CREAR USUARIO")
            print("-" * 25)

            nombre = input("USUARIO Nombre completo: ").strip()
            nombre_usuario = input("USUARIO Nombre de usuario: ").strip()
            email = input("EMAIL Email: ").strip()
            contraseña = input("PASSWORD Contraseña: ").strip()
            telefono = input("TELEFONO Teléfono (opcional): ").strip() or None
            es_admin = input("ADMIN ¿Es administrador? (s/N): ").strip().lower() == "s"

            usuario = self.usuario_crud.crear_usuario(
                nombre=nombre,
                nombre_usuario=nombre_usuario,
                email=email,
                contraseña=contraseña,
                telefono=telefono,
                es_admin=es_admin,
                id_usuario_creacion=self.auth_service.get_current_user().id,
            )

            print(f"\nOK Usuario creado exitosamente!")
            print(f"ID ID: {usuario.id}")
            print(f"USUARIO Nombre: {usuario.nombre}")
            print(f"USUARIO Usuario: {usuario.nombre_usuario}")
            print(f"EMAIL Email: {usuario.email}")
            print(f"ADMIN Admin: {'Sí' if usuario.es_admin else 'No'}")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def buscar_usuario(self):
        """Buscar un usuario."""
        try:
            self.limpiar_pantalla()
            print("DIAGNOSTICO BUSCAR USUARIO")
            print("-" * 25)

            print("1. DIAGNOSTICO Por ID")
            print("2. EMAIL Por Email")
            print("3. USUARIO Por Nombre de Usuario")
            print("4. USUARIO Por Nombre")

            opcion = input("\n-> Seleccione tipo de búsqueda: ").strip()

            if opcion == "1":
                usuario_id = input("ID Ingrese ID del usuario: ").strip()
                try:
                    usuario = self.usuario_crud.obtener_usuario(UUID(usuario_id))
                    if usuario:
                        self.mostrar_usuario(usuario)
                    else:
                        print("ERROR Usuario no encontrado")
                except ValueError:
                    print("ERROR ID inválido")

            elif opcion == "2":
                email = input("EMAIL Ingrese email: ").strip()
                usuario = self.usuario_crud.obtener_usuario_por_email(email)
                if usuario:
                    self.mostrar_usuario(usuario)
                else:
                    print("ERROR Usuario no encontrado")

            elif opcion == "3":
                nombre_usuario = input("USUARIO Ingrese nombre de usuario: ").strip()
                usuario = self.usuario_crud.obtener_usuario_por_nombre_usuario(
                    nombre_usuario
                )
                if usuario:
                    self.mostrar_usuario(usuario)
                else:
                    print("ERROR Usuario no encontrado")

            elif opcion == "4":
                nombre = input("USUARIO Ingrese nombre a buscar: ").strip()
                usuarios = self.usuario_crud.buscar_usuarios_por_nombre(nombre)
                if usuarios:
                    print(f"\nLICENCIA Encontrados {len(usuarios)} usuario(s):")
                    for usuario in usuarios:
                        self.mostrar_usuario_resumen(usuario)
                else:
                    print("ERROR No se encontraron usuarios")

            else:
                print("ERROR Opción inválida")

        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def listar_usuarios(self):
        """Listar todos los usuarios."""
        try:
            self.limpiar_pantalla()
            print("LICENCIA LISTAR USUARIOS")
            print("-" * 25)

            usuarios = self.usuario_crud.obtener_usuarios()
            if usuarios:
                print(f"\nLICENCIA Total de usuarios: {len(usuarios)}")
                for usuario in usuarios:
                    self.mostrar_usuario_resumen(usuario)
            else:
                print("ERROR No hay usuarios registrados")

        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def actualizar_usuario(self):
        """Actualizar un usuario."""
        try:
            self.limpiar_pantalla()
            print("EDITAR ACTUALIZAR USUARIO")
            print("-" * 30)

            usuario_id = input("ID Ingrese ID del usuario: ").strip()
            usuario = self.usuario_crud.obtener_usuario(UUID(usuario_id))
            if not usuario:
                print("ERROR Usuario no encontrado")
                return

            print(f"\nUSUARIO Usuario actual:")
            self.mostrar_usuario(usuario)

            print("\nEDITAR Ingrese nuevos datos (deje en blanco para mantener el actual):")

            nombre = input(f"USUARIO Nombre completo [{usuario.nombre}]: ").strip()
            nombre_usuario = input(
                f"USUARIO Nombre de usuario [{usuario.nombre_usuario}]: "
            ).strip()
            email = input(f"EMAIL Email [{usuario.email}]: ").strip()
            telefono = input(f"TELEFONO Teléfono [{usuario.telefono or 'N/A'}]: ").strip()
            es_admin = (
                input(
                    f"ADMIN ¿Es administrador? (s/N) [{'Sí' if usuario.es_admin else 'No'}]: "
                )
                .strip()
                .lower()
            )

            kwargs = {}
            if nombre:
                kwargs["nombre"] = nombre
            if nombre_usuario:
                kwargs["nombre_usuario"] = nombre_usuario
            if email:
                kwargs["email"] = email
            if telefono:
                kwargs["telefono"] = telefono
            if es_admin in ["s", "n"]:
                kwargs["es_admin"] = es_admin == "s"

            if kwargs:
                usuario_actualizado = self.usuario_crud.actualizar_usuario(
                    usuario.id, self.auth_service.get_current_user().id, **kwargs
                )
                print(f"\nOK Usuario actualizado exitosamente!")
                self.mostrar_usuario(usuario_actualizado)
            else:
                print("ℹ️ No se realizaron cambios")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def eliminar_usuario(self):
        """Eliminar un usuario."""
        try:
            self.limpiar_pantalla()
            print("ELIMINAR ELIMINAR USUARIO")
            print("-" * 25)

            usuario_id = input("ID Ingrese ID del usuario: ").strip()
            usuario = self.usuario_crud.obtener_usuario(UUID(usuario_id))
            if not usuario:
                print("ERROR Usuario no encontrado")
                return

            print(f"\nUSUARIO Usuario a eliminar:")
            self.mostrar_usuario(usuario)

            confirmacion = (
                input("\nADVERTENCIA ¿Está seguro de eliminar este usuario? (s/N): ")
                .strip()
                .lower()
            )
            if confirmacion == "s":
                if self.usuario_crud.eliminar_usuario(usuario.id):
                    print("OK Usuario eliminado exitosamente!")
                else:
                    print("ERROR Error al eliminar el usuario")
            else:
                print("ℹ️ Operación cancelada")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def cambiar_estado_usuario(self):
        """Cambiar el estado activo/inactivo de un usuario."""
        try:
            self.limpiar_pantalla()
            print("CAMBIAR CAMBIAR ESTADO DE USUARIO")
            print("-" * 35)

            usuario_id = input("ID Ingrese ID del usuario: ").strip()
            usuario = self.usuario_crud.obtener_usuario(UUID(usuario_id))
            if not usuario:
                print("ERROR Usuario no encontrado")
                return

            print(f"\nUSUARIO Usuario actual:")
            self.mostrar_usuario(usuario)

            nuevo_estado = (
                input(
                    f"\nCAMBIAR Nuevo estado (activo/inactivo) [{'activo' if usuario.activo else 'inactivo'}]: "
                )
                .strip()
                .lower()
            )
            if nuevo_estado in ["activo", "inactivo"]:
                activo = nuevo_estado == "activo"
                usuario_actualizado = self.usuario_crud.cambiar_estado_usuario(
                    usuario.id, activo, self.auth_service.get_current_user().id
                )
                print(f"\nOK Estado del usuario actualizado exitosamente!")
                print(
                    f"ESTADO Nuevo estado: {'Activo' if usuario_actualizado.activo else 'Inactivo'}"
                )
            else:
                print("ERROR Estado inválido. Use 'activo' o 'inactivo'")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def mostrar_usuario(self, usuario):
        """Mostrar información completa de un usuario."""
        print(f"\nUSUARIO INFORMACIÓN DEL USUARIO")
        print("-" * 35)
        print(f"ID ID: {usuario.id}")
        print(f"USUARIO Nombre: {usuario.nombre}")
        print(f"USUARIO Usuario: {usuario.nombre_usuario}")
        print(f"EMAIL Email: {usuario.email}")
        print(f"TELEFONO Teléfono: {usuario.telefono or 'N/A'}")
        print(f"ADMIN Administrador: {'Sí' if usuario.es_admin else 'No'}")
        print(f"ESTADO Estado: {'Activo' if usuario.activo else 'Inactivo'}")
        print(f"FECHA Creado: {usuario.created_at}")

    def mostrar_usuario_resumen(self, usuario):
        """Mostrar resumen de un usuario."""
        estado = "ACTIVO" if usuario.activo else "INACTIVO"
        admin = "ADMIN" if usuario.es_admin else "USUARIO"
        print(
            f"{estado} {admin} {usuario.id} | {usuario.nombre} | {usuario.nombre_usuario} | {usuario.email}"
        )
