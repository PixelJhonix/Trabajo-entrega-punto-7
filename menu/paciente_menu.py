"""Menú de gestión de pacientes."""

import os
from uuid import UUID
from crud.paciente_crud import PacienteCRUD


class PacienteMenu:
    """Menú para gestión de pacientes."""

    def __init__(self, db, auth_service):
        self.db = db
        self.auth_service = auth_service
        self.paciente_crud = PacienteCRUD(db)

    def limpiar_pantalla(self):
        """Limpiar la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_titulo(self):
        """Mostrar título del módulo."""
        print("👥 GESTIÓN DE PACIENTES")
        print("=" * 40)

    def mostrar_menu(self):
        """Mostrar menú de pacientes."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                print("\n📋 OPCIONES DISPONIBLES")
                print("-" * 25)
                print("1. ➕ Registrar Nuevo Paciente")
                print("2. 🔍 Buscar Paciente")
                print("3. 📋 Listar Pacientes")
                print("4. ✏️ Actualizar Paciente")
                print("5. 🗑️ Eliminar Paciente")
                print("0. 🔙 Volver al Menú Principal")

                opcion = input("\n🔹 Seleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.registrar_paciente()
                elif opcion == "2":
                    self.buscar_paciente()
                elif opcion == "3":
                    self.listar_pacientes()
                elif opcion == "4":
                    self.actualizar_paciente()
                elif opcion == "5":
                    self.eliminar_paciente()
                else:
                    print("❌ Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Presione Enter para continuar...")

    def registrar_paciente(self):
        """Registrar un nuevo paciente."""
        self.limpiar_pantalla()
        print("➕ REGISTRAR NUEVO PACIENTE")
        print("-" * 35)

        try:
            primer_nombre = input("👤 Primer nombre: ").strip()
            if not primer_nombre:
                print("❌ El primer nombre es obligatorio")
                input("Presione Enter para continuar...")
                return

            segundo_nombre = input("👤 Segundo nombre (opcional): ").strip()
            if not segundo_nombre:
                segundo_nombre = None

            apellido = input("👤 Apellido: ").strip()
            if not apellido:
                print("❌ El apellido es obligatorio")
                input("Presione Enter para continuar...")
                return

            fecha_nacimiento = input("📅 Fecha de nacimiento (YYYY-MM-DD): ").strip()
            if not fecha_nacimiento:
                print("❌ La fecha de nacimiento es obligatoria")
                input("Presione Enter para continuar...")
                return

            telefono = input("📞 Teléfono: ").strip()
            if not telefono:
                print("❌ El teléfono es obligatorio")
                input("Presione Enter para continuar...")
                return

            email = input("📧 Email (opcional): ").strip()
            if not email:
                email = None

            direccion = input("🏠 Dirección: ").strip()
            if not direccion:
                print("❌ La dirección es obligatoria")
                input("Presione Enter para continuar...")
                return

            # Obtener ID del usuario actual
            usuario_actual = self.auth_service.usuario_actual
            if not usuario_actual:
                print("❌ No hay usuario autenticado")
                input("Presione Enter para continuar...")
                return

            paciente = self.paciente_crud.crear_paciente(
                primer_nombre=primer_nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                direccion=direccion,
                id_usuario_creacion=usuario_actual.id,
                segundo_nombre=segundo_nombre,
                email=email,
            )

            print(f"\n✅ Paciente registrado exitosamente!")
            print(f"🆔 ID: {paciente.id}")
            print(f"👤 Nombre: {paciente.primer_nombre} {paciente.apellido}")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def buscar_paciente(self):
        """Buscar un paciente."""
        self.limpiar_pantalla()
        print("🔍 BUSCAR PACIENTE")
        print("-" * 25)

        try:
            print("Opciones de búsqueda:")
            print("1. Por ID")
            print("2. Por email")
            print("3. Por nombre")

            opcion = input("\n🔹 Seleccione una opción: ").strip()

            if opcion == "1":
                paciente_id = input("🆔 ID del paciente: ").strip()
                if not paciente_id:
                    print("❌ El ID es obligatorio")
                    input("Presione Enter para continuar...")
                    return

                try:
                    paciente = self.paciente_crud.obtener_paciente(UUID(paciente_id))
                    if paciente:
                        self.mostrar_paciente(paciente)
                    else:
                        print("❌ Paciente no encontrado")
                except ValueError:
                    print("❌ ID inválido")

            elif opcion == "2":
                email = input("📧 Email del paciente: ").strip()
                if not email:
                    print("❌ El email es obligatorio")
                    input("Presione Enter para continuar...")
                    return

                paciente = self.paciente_crud.obtener_paciente_por_email(email)
                if paciente:
                    self.mostrar_paciente(paciente)
                else:
                    print("❌ Paciente no encontrado")

            elif opcion == "3":
                nombre = input("👤 Nombre a buscar: ").strip()
                if not nombre:
                    print("❌ El nombre es obligatorio")
                    input("Presione Enter para continuar...")
                    return

                pacientes = self.paciente_crud.buscar_pacientes_por_nombre(nombre)
                if pacientes:
                    print(f"\n📋 Se encontraron {len(pacientes)} paciente(s):")
                    for i, paciente in enumerate(pacientes, 1):
                        print(
                            f"{i}. {paciente.primer_nombre} {paciente.apellido} (ID: {paciente.id})"
                        )
                else:
                    print("❌ No se encontraron pacientes")

            else:
                print("❌ Opción inválida")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def listar_pacientes(self):
        """Listar todos los pacientes."""
        self.limpiar_pantalla()
        print("📋 LISTA DE PACIENTES")
        print("-" * 25)

        try:
            pacientes = self.paciente_crud.obtener_pacientes()
            if pacientes:
                print(f"\n📊 Total de pacientes: {len(pacientes)}")
                print("-" * 60)
                for i, paciente in enumerate(pacientes, 1):
                    print(f"{i:2d}. {paciente.primer_nombre} {paciente.apellido}")
                    print(f"     📧 Email: {paciente.email or 'No especificado'}")
                    print(f"     📞 Teléfono: {paciente.telefono}")
                    print(f"     🆔 ID: {paciente.id}")
                    print("-" * 60)
            else:
                print("📭 No hay pacientes registrados")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def actualizar_paciente(self):
        """Actualizar un paciente."""
        self.limpiar_pantalla()
        print("✏️ ACTUALIZAR PACIENTE")
        print("-" * 30)

        try:
            paciente_id = input("🆔 ID del paciente: ").strip()
            if not paciente_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            paciente = self.paciente_crud.obtener_paciente(UUID(paciente_id))
            if not paciente:
                print("❌ Paciente no encontrado")
                input("Presione Enter para continuar...")
                return

            print(f"\n👤 Paciente: {paciente.primer_nombre} {paciente.apellido}")
            print("Deje en blanco para mantener el valor actual\n")

            # Campos a actualizar
            campos = {}

            nuevo_primer_nombre = input(
                f"👤 Primer nombre [{paciente.primer_nombre}]: "
            ).strip()
            if nuevo_primer_nombre:
                campos["primer_nombre"] = nuevo_primer_nombre

            nuevo_apellido = input(f"👤 Apellido [{paciente.apellido}]: ").strip()
            if nuevo_apellido:
                campos["apellido"] = nuevo_apellido

            nuevo_telefono = input(f"📞 Teléfono [{paciente.telefono}]: ").strip()
            if nuevo_telefono:
                campos["telefono"] = nuevo_telefono

            nuevo_email = input(
                f"📧 Email [{paciente.email or 'No especificado'}]: "
            ).strip()
            if nuevo_email:
                campos["email"] = nuevo_email

            nueva_direccion = input(f"🏠 Dirección [{paciente.direccion}]: ").strip()
            if nueva_direccion:
                campos["direccion"] = nueva_direccion

            if campos:
                usuario_actual = self.auth_service.usuario_actual
                paciente_actualizado = self.paciente_crud.actualizar_paciente(
                    UUID(paciente_id), usuario_actual.id, **campos
                )
                print(f"\n✅ Paciente actualizado exitosamente!")
            else:
                print("ℹ️ No se realizaron cambios")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def eliminar_paciente(self):
        """Eliminar un paciente."""
        self.limpiar_pantalla()
        print("🗑️ ELIMINAR PACIENTE")
        print("-" * 25)

        try:
            paciente_id = input("🆔 ID del paciente: ").strip()
            if not paciente_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            paciente = self.paciente_crud.obtener_paciente(UUID(paciente_id))
            if not paciente:
                print("❌ Paciente no encontrado")
                input("Presione Enter para continuar...")
                return

            print(f"\n⚠️ ADVERTENCIA: Esta acción no se puede deshacer")
            print(f"👤 Paciente: {paciente.primer_nombre} {paciente.apellido}")

            confirmar = (
                input("\n¿Está seguro de eliminar este paciente? (s/N): ")
                .strip()
                .lower()
            )
            if confirmar in ["s", "si", "sí", "y", "yes"]:
                if self.paciente_crud.eliminar_paciente(UUID(paciente_id)):
                    print("✅ Paciente eliminado exitosamente")
                else:
                    print("❌ Error al eliminar el paciente")
            else:
                print("ℹ️ Operación cancelada")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def mostrar_paciente(self, paciente):
        """Mostrar información de un paciente."""
        print(f"\n👤 INFORMACIÓN DEL PACIENTE")
        print("-" * 35)
        print(f"🆔 ID: {paciente.id}")
        print(f"👤 Nombre: {paciente.primer_nombre} {paciente.apellido}")
        if paciente.segundo_nombre:
            print(f"👤 Segundo nombre: {paciente.segundo_nombre}")
        print(f"📅 Fecha de nacimiento: {paciente.fecha_nacimiento}")
        print(f"📞 Teléfono: {paciente.telefono}")
        print(f"📧 Email: {paciente.email or 'No especificado'}")
        print(f"🏠 Dirección: {paciente.direccion}")
        print(f"📅 Registrado: {paciente.created_at}")
