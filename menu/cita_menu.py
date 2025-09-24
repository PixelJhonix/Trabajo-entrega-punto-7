"""Menú de gestión de citas."""

import os
from uuid import UUID
from crud.cita_crud import CitaCRUD


class CitaMenu:
    """Menú para gestión de citas."""

    def __init__(self, db, auth_service):
        self.db = db
        self.auth_service = auth_service
        self.cita_crud = CitaCRUD(db)

    def limpiar_pantalla(self):
        """Limpiar la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_titulo(self):
        """Mostrar título del módulo."""
        print("📅 GESTIÓN DE CITAS")
        print("=" * 40)

    def mostrar_menu(self):
        """Mostrar menú de citas."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                print("\n📋 OPCIONES DISPONIBLES")
                print("-" * 25)
                print("1. ➕ Agendar Nueva Cita")
                print("2. 🔍 Buscar Cita")
                print("3. 📋 Listar Citas")
                print("4. ✏️ Actualizar Cita")
                print("5. ❌ Cancelar Cita")
                print("6. ✅ Completar Cita")
                print("0. 🔙 Volver al Menú Principal")

                opcion = input("\n🔹 Seleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.agendar_cita()
                elif opcion == "2":
                    self.buscar_cita()
                elif opcion == "3":
                    self.listar_citas()
                elif opcion == "4":
                    self.actualizar_cita()
                elif opcion == "5":
                    self.cancelar_cita()
                elif opcion == "6":
                    self.completar_cita()
                else:
                    print("❌ Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Presione Enter para continuar...")

    def agendar_cita(self):
        """Agendar una nueva cita."""
        self.limpiar_pantalla()
        print("➕ AGENDAR NUEVA CITA")
        print("-" * 35)

        try:
            paciente_id = input("🆔 ID del paciente: ").strip()
            if not paciente_id:
                print("❌ El ID del paciente es obligatorio")
                input("Presione Enter para continuar...")
                return

            medico_id = input("🆔 ID del médico: ").strip()
            if not medico_id:
                print("❌ El ID del médico es obligatorio")
                input("Presione Enter para continuar...")
                return

            fecha = input("📅 Fecha (YYYY-MM-DD): ").strip()
            if not fecha:
                print("❌ La fecha es obligatoria")
                input("Presione Enter para continuar...")
                return

            hora = input("🕐 Hora (HH:MM:SS): ").strip()
            if not hora:
                print("❌ La hora es obligatoria")
                input("Presione Enter para continuar...")
                return

            motivo = input("📝 Motivo de la consulta: ").strip()
            if not motivo:
                print("❌ El motivo es obligatorio")
                input("Presione Enter para continuar...")
                return

            observaciones = input("📄 Observaciones (opcional): ").strip()
            if not observaciones:
                observaciones = None

            usuario_actual = self.auth_service.usuario_actual
            if not usuario_actual:
                print("❌ No hay usuario autenticado")
                input("Presione Enter para continuar...")
                return

            cita = self.cita_crud.crear_cita(
                paciente_id=UUID(paciente_id),
                medico_id=UUID(medico_id),
                fecha=fecha,
                hora=hora,
                motivo=motivo,
                id_usuario_creacion=usuario_actual.id,
                observaciones=observaciones,
            )

            print(f"\n✅ Cita agendada exitosamente!")
            print(f"🆔 ID: {cita.id}")
            print(f"📅 Fecha: {cita.fecha}")
            print(f"🕐 Hora: {cita.hora}")
            print(f"📝 Motivo: {cita.motivo}")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def buscar_cita(self):
        """Buscar una cita."""
        self.limpiar_pantalla()
        print("🔍 BUSCAR CITA")
        print("-" * 25)

        try:
            cita_id = input("🆔 ID de la cita: ").strip()
            if not cita_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            cita = self.cita_crud.obtener_cita(UUID(cita_id))
            if cita:
                self.mostrar_cita(cita)
            else:
                print("❌ Cita no encontrada")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def listar_citas(self):
        """Listar todas las citas."""
        self.limpiar_pantalla()
        print("📋 LISTA DE CITAS")
        print("-" * 25)

        try:
            citas = self.cita_crud.obtener_citas()
            if citas:
                print(f"\n📊 Total de citas: {len(citas)}")
                print("-" * 80)
                for i, cita in enumerate(citas, 1):
                    print(f"{i:2d}. Cita #{cita.id}")
                    print(f"     📅 Fecha: {cita.fecha} - {cita.hora}")
                    print(f"     📝 Motivo: {cita.motivo}")
                    print(f"     📊 Estado: {cita.estado}")
                    print(f"     🆔 ID: {cita.id}")
                    print("-" * 80)
            else:
                print("📭 No hay citas registradas")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def actualizar_cita(self):
        """Actualizar una cita."""
        self.limpiar_pantalla()
        print("✏️ ACTUALIZAR CITA")
        print("-" * 30)

        try:
            cita_id = input("🆔 ID de la cita: ").strip()
            if not cita_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            cita = self.cita_crud.obtener_cita(UUID(cita_id))
            if not cita:
                print("❌ Cita no encontrada")
                input("Presione Enter para continuar...")
                return

            print(f"\n📅 Cita: {cita.fecha} - {cita.hora}")
            print("Deje en blanco para mantener el valor actual\n")

            campos = {}

            nuevo_motivo = input(f"📝 Motivo [{cita.motivo}]: ").strip()
            if nuevo_motivo:
                campos["motivo"] = nuevo_motivo

            nuevo_estado = input(f"📊 Estado [{cita.estado}]: ").strip()
            if nuevo_estado:
                campos["estado"] = nuevo_estado

            nuevas_observaciones = input(
                f"📄 Observaciones [{cita.observaciones or 'Ninguna'}]: "
            ).strip()
            if nuevas_observaciones:
                campos["observaciones"] = nuevas_observaciones

            if campos:
                usuario_actual = self.auth_service.usuario_actual
                cita_actualizada = self.cita_crud.actualizar_cita(
                    UUID(cita_id), usuario_actual.id, **campos
                )
                print(f"\n✅ Cita actualizada exitosamente!")
            else:
                print("ℹ️ No se realizaron cambios")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def cancelar_cita(self):
        """Cancelar una cita."""
        self.limpiar_pantalla()
        print("❌ CANCELAR CITA")
        print("-" * 25)

        try:
            cita_id = input("🆔 ID de la cita: ").strip()
            if not cita_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            cita = self.cita_crud.obtener_cita(UUID(cita_id))
            if not cita:
                print("❌ Cita no encontrada")
                input("Presione Enter para continuar...")
                return

            print(f"\n📅 Cita: {cita.fecha} - {cita.hora}")
            print(f"📝 Motivo: {cita.motivo}")

            confirmar = (
                input("\n¿Está seguro de cancelar esta cita? (s/N): ").strip().lower()
            )
            if confirmar in ["s", "si", "sí", "y", "yes"]:
                usuario_actual = self.auth_service.usuario_actual
                if self.cita_crud.cancelar_cita(UUID(cita_id), usuario_actual.id):
                    print("✅ Cita cancelada exitosamente")
                else:
                    print("❌ Error al cancelar la cita")
            else:
                print("ℹ️ Operación cancelada")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def completar_cita(self):
        """Completar una cita."""
        self.limpiar_pantalla()
        print("✅ COMPLETAR CITA")
        print("-" * 25)

        try:
            cita_id = input("🆔 ID de la cita: ").strip()
            if not cita_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            cita = self.cita_crud.obtener_cita(UUID(cita_id))
            if not cita:
                print("❌ Cita no encontrada")
                input("Presione Enter para continuar...")
                return

            print(f"\n📅 Cita: {cita.fecha} - {cita.hora}")
            print(f"📝 Motivo: {cita.motivo}")

            confirmar = (
                input("\n¿Está seguro de marcar esta cita como completada? (s/N): ")
                .strip()
                .lower()
            )
            if confirmar in ["s", "si", "sí", "y", "yes"]:
                usuario_actual = self.auth_service.usuario_actual
                if self.cita_crud.completar_cita(UUID(cita_id), usuario_actual.id):
                    print("✅ Cita completada exitosamente")
                else:
                    print("❌ Error al completar la cita")
            else:
                print("ℹ️ Operación cancelada")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def mostrar_cita(self, cita):
        """Mostrar información de una cita."""
        print(f"\n📅 INFORMACIÓN DE LA CITA")
        print("-" * 35)
        print(f"🆔 ID: {cita.id}")
        print(f"📅 Fecha: {cita.fecha}")
        print(f"🕐 Hora: {cita.hora}")
        print(f"📝 Motivo: {cita.motivo}")
        print(f"📊 Estado: {cita.estado}")
        if cita.observaciones:
            print(f"📄 Observaciones: {cita.observaciones}")
        print(f"📅 Creada: {cita.created_at}")
