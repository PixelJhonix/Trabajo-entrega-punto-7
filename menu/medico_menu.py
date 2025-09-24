"""Menú de gestión de médicos."""

import os
from uuid import UUID
from crud.medico_crud import MedicoCRUD


class MedicoMenu:
    """Menú para gestión de médicos."""

    def __init__(self, db, auth_service):
        self.db = db
        self.auth_service = auth_service
        self.medico_crud = MedicoCRUD(db)

    def limpiar_pantalla(self):
        """Limpiar la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_titulo(self):
        """Mostrar título del módulo."""
        print("👨‍⚕️ GESTIÓN DE MÉDICOS")
        print("=" * 40)

    def mostrar_menu(self):
        """Mostrar menú de médicos."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                print("\n📋 OPCIONES DISPONIBLES")
                print("-" * 25)
                print("1. ➕ Registrar Nuevo Médico")
                print("2. 🔍 Buscar Médico")
                print("3. 📋 Listar Médicos")
                print("4. ✏️ Actualizar Médico")
                print("5. 🗑️ Eliminar Médico")
                print("0. 🔙 Volver al Menú Principal")

                opcion = input("\n🔹 Seleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.registrar_medico()
                elif opcion == "2":
                    self.buscar_medico()
                elif opcion == "3":
                    self.listar_medicos()
                elif opcion == "4":
                    self.actualizar_medico()
                elif opcion == "5":
                    self.eliminar_medico()
                else:
                    print("❌ Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Presione Enter para continuar...")

    def registrar_medico(self):
        """Registrar un nuevo médico."""
        self.limpiar_pantalla()
        print("➕ REGISTRAR NUEVO MÉDICO")
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

            especialidad = input("🩺 Especialidad: ").strip()
            if not especialidad:
                print("❌ La especialidad es obligatoria")
                input("Presione Enter para continuar...")
                return

            numero_licencia = input("📜 Número de licencia: ").strip()
            if not numero_licencia:
                print("❌ El número de licencia es obligatorio")
                input("Presione Enter para continuar...")
                return

            consultorio = input("🏥 Consultorio (opcional): ").strip()
            if not consultorio:
                consultorio = None

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

            usuario_actual = self.auth_service.usuario_actual
            if not usuario_actual:
                print("❌ No hay usuario autenticado")
                input("Presione Enter para continuar...")
                return

            medico = self.medico_crud.crear_medico(
                primer_nombre=primer_nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                especialidad=especialidad,
                numero_licencia=numero_licencia,
                telefono=telefono,
                direccion=direccion,
                id_usuario_creacion=usuario_actual.id,
                segundo_nombre=segundo_nombre,
                consultorio=consultorio,
                email=email,
            )

            print(f"\n✅ Médico registrado exitosamente!")
            print(f"🆔 ID: {medico.id}")
            print(f"👤 Nombre: Dr. {medico.primer_nombre} {medico.apellido}")
            print(f"🩺 Especialidad: {medico.especialidad}")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def buscar_medico(self):
        """Buscar un médico."""
        self.limpiar_pantalla()
        print("🔍 BUSCAR MÉDICO")
        print("-" * 25)

        try:
            print("Opciones de búsqueda:")
            print("1. Por ID")
            print("2. Por email")
            print("3. Por nombre")
            print("4. Por especialidad")

            opcion = input("\n🔹 Seleccione una opción: ").strip()

            if opcion == "1":
                medico_id = input("🆔 ID del médico: ").strip()
                if not medico_id:
                    print("❌ El ID es obligatorio")
                    input("Presione Enter para continuar...")
                    return

                try:
                    medico = self.medico_crud.obtener_medico(UUID(medico_id))
                    if medico:
                        self.mostrar_medico(medico)
                    else:
                        print("❌ Médico no encontrado")
                except ValueError:
                    print("❌ ID inválido")

            elif opcion == "2":
                email = input("📧 Email del médico: ").strip()
                if not email:
                    print("❌ El email es obligatorio")
                    input("Presione Enter para continuar...")
                    return

                medico = self.medico_crud.obtener_medico_por_email(email)
                if medico:
                    self.mostrar_medico(medico)
                else:
                    print("❌ Médico no encontrado")

            elif opcion == "3":
                nombre = input("👤 Nombre a buscar: ").strip()
                if not nombre:
                    print("❌ El nombre es obligatorio")
                    input("Presione Enter para continuar...")
                    return

                medicos = self.medico_crud.buscar_medicos_por_nombre(nombre)
                if medicos:
                    print(f"\n📋 Se encontraron {len(medicos)} médico(s):")
                    for i, medico in enumerate(medicos, 1):
                        print(
                            f"{i}. Dr. {medico.primer_nombre} {medico.apellido} - {medico.especialidad}"
                        )
                else:
                    print("❌ No se encontraron médicos")

            elif opcion == "4":
                especialidad = input("🩺 Especialidad a buscar: ").strip()
                if not especialidad:
                    print("❌ La especialidad es obligatoria")
                    input("Presione Enter para continuar...")
                    return

                medicos = self.medico_crud.obtener_medicos_por_especialidad(
                    especialidad
                )
                if medicos:
                    print(
                        f"\n📋 Se encontraron {len(medicos)} médico(s) de {especialidad}:"
                    )
                    for i, medico in enumerate(medicos, 1):
                        print(f"{i}. Dr. {medico.primer_nombre} {medico.apellido}")
                else:
                    print("❌ No se encontraron médicos de esa especialidad")

            else:
                print("❌ Opción inválida")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def listar_medicos(self):
        """Listar todos los médicos."""
        self.limpiar_pantalla()
        print("📋 LISTA DE MÉDICOS")
        print("-" * 25)

        try:
            medicos = self.medico_crud.obtener_medicos()
            if medicos:
                print(f"\n📊 Total de médicos: {len(medicos)}")
                print("-" * 80)
                for i, medico in enumerate(medicos, 1):
                    print(f"{i:2d}. Dr. {medico.primer_nombre} {medico.apellido}")
                    print(f"     🩺 Especialidad: {medico.especialidad}")
                    print(f"     📜 Licencia: {medico.numero_licencia}")
                    print(f"     📧 Email: {medico.email or 'No especificado'}")
                    print(f"     🆔 ID: {medico.id}")
                    print("-" * 80)
            else:
                print("📭 No hay médicos registrados")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def actualizar_medico(self):
        """Actualizar un médico."""
        self.limpiar_pantalla()
        print("✏️ ACTUALIZAR MÉDICO")
        print("-" * 30)

        try:
            medico_id = input("🆔 ID del médico: ").strip()
            if not medico_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            medico = self.medico_crud.obtener_medico(UUID(medico_id))
            if not medico:
                print("❌ Médico no encontrado")
                input("Presione Enter para continuar...")
                return

            print(f"\n👤 Médico: Dr. {medico.primer_nombre} {medico.apellido}")
            print("Deje en blanco para mantener el valor actual\n")

            campos = {}

            nuevo_primer_nombre = input(
                f"👤 Primer nombre [{medico.primer_nombre}]: "
            ).strip()
            if nuevo_primer_nombre:
                campos["primer_nombre"] = nuevo_primer_nombre

            nuevo_apellido = input(f"👤 Apellido [{medico.apellido}]: ").strip()
            if nuevo_apellido:
                campos["apellido"] = nuevo_apellido

            nueva_especialidad = input(
                f"🩺 Especialidad [{medico.especialidad}]: "
            ).strip()
            if nueva_especialidad:
                campos["especialidad"] = nueva_especialidad

            nuevo_telefono = input(f"📞 Teléfono [{medico.telefono}]: ").strip()
            if nuevo_telefono:
                campos["telefono"] = nuevo_telefono

            nuevo_email = input(
                f"📧 Email [{medico.email or 'No especificado'}]: "
            ).strip()
            if nuevo_email:
                campos["email"] = nuevo_email

            nueva_direccion = input(f"🏠 Dirección [{medico.direccion}]: ").strip()
            if nueva_direccion:
                campos["direccion"] = nueva_direccion

            if campos:
                usuario_actual = self.auth_service.usuario_actual
                medico_actualizado = self.medico_crud.actualizar_medico(
                    UUID(medico_id), usuario_actual.id, **campos
                )
                print(f"\n✅ Médico actualizado exitosamente!")
            else:
                print("ℹ️ No se realizaron cambios")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def eliminar_medico(self):
        """Eliminar un médico."""
        self.limpiar_pantalla()
        print("🗑️ ELIMINAR MÉDICO")
        print("-" * 25)

        try:
            medico_id = input("🆔 ID del médico: ").strip()
            if not medico_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            medico = self.medico_crud.obtener_medico(UUID(medico_id))
            if not medico:
                print("❌ Médico no encontrado")
                input("Presione Enter para continuar...")
                return

            print(f"\n⚠️ ADVERTENCIA: Esta acción no se puede deshacer")
            print(f"👤 Médico: Dr. {medico.primer_nombre} {medico.apellido}")
            print(f"🩺 Especialidad: {medico.especialidad}")

            confirmar = (
                input("\n¿Está seguro de eliminar este médico? (s/N): ").strip().lower()
            )
            if confirmar in ["s", "si", "sí", "y", "yes"]:
                if self.medico_crud.eliminar_medico(UUID(medico_id)):
                    print("✅ Médico eliminado exitosamente")
                else:
                    print("❌ Error al eliminar el médico")
            else:
                print("ℹ️ Operación cancelada")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def mostrar_medico(self, medico):
        """Mostrar información de un médico."""
        print(f"\n👨‍⚕️ INFORMACIÓN DEL MÉDICO")
        print("-" * 35)
        print(f"🆔 ID: {medico.id}")
        print(f"👤 Nombre: Dr. {medico.primer_nombre} {medico.apellido}")
        if medico.segundo_nombre:
            print(f"👤 Segundo nombre: {medico.segundo_nombre}")
        print(f"🩺 Especialidad: {medico.especialidad}")
        print(f"📜 Licencia: {medico.numero_licencia}")
        if medico.consultorio:
            print(f"🏥 Consultorio: {medico.consultorio}")
        print(f"📞 Teléfono: {medico.telefono}")
        print(f"📧 Email: {medico.email or 'No especificado'}")
        print(f"🏠 Dirección: {medico.direccion}")
        print(f"📅 Registrado: {medico.created_at}")
