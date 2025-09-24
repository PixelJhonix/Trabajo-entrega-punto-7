"""Menú de gestión de hospitalizaciones."""

import os
from uuid import UUID
from crud.hospitalizacion_crud import HospitalizacionCRUD


class HospitalizacionMenu:
    """Menú para gestión de hospitalizaciones."""

    def __init__(self, db, auth_service):
        self.db = db
        self.auth_service = auth_service
        self.hospitalizacion_crud = HospitalizacionCRUD(db)

    def limpiar_pantalla(self):
        """Limpiar la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_titulo(self):
        """Mostrar título del módulo."""
        print("🏥 GESTIÓN DE HOSPITALIZACIONES")
        print("=" * 40)

    def mostrar_menu(self):
        """Mostrar menú de hospitalizaciones."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                print("\n📋 OPCIONES DISPONIBLES")
                print("-" * 25)
                print("1. ➕ Registrar Nueva Hospitalización")
                print("2. 🔍 Buscar Hospitalización")
                print("3. 📋 Listar Hospitalizaciones")
                print("4. ✏️ Actualizar Hospitalización")
                print("5. ✅ Completar Hospitalización")
                print("6. ❌ Cancelar Hospitalización")
                print("0. 🔙 Volver al Menú Principal")

                opcion = input("\n🔹 Seleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.registrar_hospitalizacion()
                elif opcion == "2":
                    self.buscar_hospitalizacion()
                elif opcion == "3":
                    self.listar_hospitalizaciones()
                elif opcion == "4":
                    self.actualizar_hospitalizacion()
                elif opcion == "5":
                    self.completar_hospitalizacion()
                elif opcion == "6":
                    self.cancelar_hospitalizacion()
                else:
                    print("❌ Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Presione Enter para continuar...")

    def registrar_hospitalizacion(self):
        """Registrar una nueva hospitalización."""
        self.limpiar_pantalla()
        print("➕ REGISTRAR NUEVA HOSPITALIZACIÓN")
        print("-" * 45)

        try:
            paciente_id = input("🆔 ID del paciente: ").strip()
            if not paciente_id:
                print("❌ El ID del paciente es obligatorio")
                input("Presione Enter para continuar...")
                return

            medico_id = input("🆔 ID del médico responsable: ").strip()
            if not medico_id:
                print("❌ El ID del médico es obligatorio")
                input("Presione Enter para continuar...")
                return

            enfermera_id = input("🆔 ID de la enfermera (opcional): ").strip()
            if not enfermera_id:
                enfermera_id = None

            tipo_cuidado = input(
                "🏥 Tipo de cuidado (Intensivo/Intermedio/Básico): "
            ).strip()
            if not tipo_cuidado:
                print("❌ El tipo de cuidado es obligatorio")
                input("Presione Enter para continuar...")
                return

            descripcion = input("📝 Descripción: ").strip()
            if not descripcion:
                print("❌ La descripción es obligatoria")
                input("Presione Enter para continuar...")
                return

            numero_habitacion = input("🏠 Número de habitación: ").strip()
            if not numero_habitacion:
                print("❌ El número de habitación es obligatorio")
                input("Presione Enter para continuar...")
                return

            tipo_habitacion = input(
                "🏠 Tipo de habitación (Individual/Compartida/ICU): "
            ).strip()
            if not tipo_habitacion:
                print("❌ El tipo de habitación es obligatorio")
                input("Presione Enter para continuar...")
                return

            fecha_inicio = input("📅 Fecha de inicio (YYYY-MM-DD): ").strip()
            if not fecha_inicio:
                print("❌ La fecha de inicio es obligatoria")
                input("Presione Enter para continuar...")
                return

            fecha_fin = input("📅 Fecha de fin (opcional, YYYY-MM-DD): ").strip()
            if not fecha_fin:
                fecha_fin = None

            usuario_actual = self.auth_service.usuario_actual
            if not usuario_actual:
                print("❌ No hay usuario autenticado")
                input("Presione Enter para continuar...")
                return

            hospitalizacion = self.hospitalizacion_crud.crear_hospitalizacion(
                paciente_id=UUID(paciente_id),
                medico_responsable_id=UUID(medico_id),
                tipo_cuidado=tipo_cuidado,
                descripcion=descripcion,
                numero_habitacion=numero_habitacion,
                tipo_habitacion=tipo_habitacion,
                fecha_inicio=fecha_inicio,
                id_usuario_creacion=usuario_actual.id,
                enfermera_asignada_id=UUID(enfermera_id) if enfermera_id else None,
                fecha_fin=fecha_fin,
            )

            print(f"\n✅ Hospitalización registrada exitosamente!")
            print(f"🆔 ID: {hospitalizacion.id}")
            print(f"🏠 Habitación: {hospitalizacion.numero_habitacion}")
            print(f"🏥 Tipo: {hospitalizacion.tipo_cuidado}")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def buscar_hospitalizacion(self):
        """Buscar una hospitalización."""
        self.limpiar_pantalla()
        print("🔍 BUSCAR HOSPITALIZACIÓN")
        print("-" * 35)

        try:
            hospitalizacion_id = input("🆔 ID de la hospitalización: ").strip()
            if not hospitalizacion_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            hospitalizacion = self.hospitalizacion_crud.obtener_hospitalizacion(
                UUID(hospitalizacion_id)
            )
            if hospitalizacion:
                self.mostrar_hospitalizacion(hospitalizacion)
            else:
                print("❌ Hospitalización no encontrada")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def listar_hospitalizaciones(self):
        """Listar todas las hospitalizaciones."""
        self.limpiar_pantalla()
        print("📋 LISTA DE HOSPITALIZACIONES")
        print("-" * 35)

        try:
            hospitalizaciones = self.hospitalizacion_crud.obtener_hospitalizaciones()
            if hospitalizaciones:
                print(f"\n📊 Total de hospitalizaciones: {len(hospitalizaciones)}")
                print("-" * 80)
                for i, hosp in enumerate(hospitalizaciones, 1):
                    print(f"{i:2d}. Hospitalización #{hosp.id}")
                    print(f"     🏠 Habitación: {hosp.numero_habitacion}")
                    print(f"     🏥 Tipo: {hosp.tipo_cuidado}")
                    print(f"     📊 Estado: {hosp.estado}")
                    print(f"     📅 Inicio: {hosp.fecha_inicio}")
                    if hosp.fecha_fin:
                        print(f"     📅 Fin: {hosp.fecha_fin}")
                    print("-" * 80)
            else:
                print("📭 No hay hospitalizaciones registradas")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def actualizar_hospitalizacion(self):
        """Actualizar una hospitalización."""
        self.limpiar_pantalla()
        print("✏️ ACTUALIZAR HOSPITALIZACIÓN")
        print("-" * 40)

        try:
            hospitalizacion_id = input("🆔 ID de la hospitalización: ").strip()
            if not hospitalizacion_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            hospitalizacion = self.hospitalizacion_crud.obtener_hospitalizacion(
                UUID(hospitalizacion_id)
            )
            if not hospitalizacion:
                print("❌ Hospitalización no encontrada")
                input("Presione Enter para continuar...")
                return

            print(f"\n🏥 Hospitalización: {hospitalizacion.numero_habitacion}")
            print("Deje en blanco para mantener el valor actual\n")

            campos = {}

            nuevo_estado = input(f"📊 Estado [{hospitalizacion.estado}]: ").strip()
            if nuevo_estado:
                campos["estado"] = nuevo_estado

            nueva_descripcion = input(
                f"📝 Descripción [{hospitalizacion.descripcion}]: "
            ).strip()
            if nueva_descripcion:
                campos["descripcion"] = nueva_descripcion

            if campos:
                usuario_actual = self.auth_service.usuario_actual
                hosp_actualizada = self.hospitalizacion_crud.actualizar_hospitalizacion(
                    UUID(hospitalizacion_id), usuario_actual.id, **campos
                )
                print(f"\n✅ Hospitalización actualizada exitosamente!")
            else:
                print("ℹ️ No se realizaron cambios")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def completar_hospitalizacion(self):
        """Completar una hospitalización."""
        self.limpiar_pantalla()
        print("✅ COMPLETAR HOSPITALIZACIÓN")
        print("-" * 35)

        try:
            hospitalizacion_id = input("🆔 ID de la hospitalización: ").strip()
            if not hospitalizacion_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            fecha_fin = input("📅 Fecha de fin (YYYY-MM-DD): ").strip()
            if not fecha_fin:
                print("❌ La fecha de fin es obligatoria")
                input("Presione Enter para continuar...")
                return

            usuario_actual = self.auth_service.usuario_actual
            if self.hospitalizacion_crud.completar_hospitalizacion(
                UUID(hospitalizacion_id), fecha_fin, usuario_actual.id
            ):
                print("✅ Hospitalización completada exitosamente")
            else:
                print("❌ Error al completar la hospitalización")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def cancelar_hospitalizacion(self):
        """Cancelar una hospitalización."""
        self.limpiar_pantalla()
        print("❌ CANCELAR HOSPITALIZACIÓN")
        print("-" * 35)

        try:
            hospitalizacion_id = input("🆔 ID de la hospitalización: ").strip()
            if not hospitalizacion_id:
                print("❌ El ID es obligatorio")
                input("Presione Enter para continuar...")
                return

            hospitalizacion = self.hospitalizacion_crud.obtener_hospitalizacion(
                UUID(hospitalizacion_id)
            )
            if not hospitalizacion:
                print("❌ Hospitalización no encontrada")
                input("Presione Enter para continuar...")
                return

            print(f"\n🏥 Hospitalización: {hospitalizacion.numero_habitacion}")
            print(f"📊 Estado: {hospitalizacion.estado}")

            confirmar = (
                input("\n¿Está seguro de cancelar esta hospitalización? (s/N): ")
                .strip()
                .lower()
            )
            if confirmar in ["s", "si", "sí", "y", "yes"]:
                usuario_actual = self.auth_service.usuario_actual
                if self.hospitalizacion_crud.cancelar_hospitalizacion(
                    UUID(hospitalizacion_id), usuario_actual.id
                ):
                    print("✅ Hospitalización cancelada exitosamente")
                else:
                    print("❌ Error al cancelar la hospitalización")
            else:
                print("ℹ️ Operación cancelada")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPresione Enter para continuar...")

    def mostrar_hospitalizacion(self, hospitalizacion):
        """Mostrar información de una hospitalización."""
        print(f"\n🏥 INFORMACIÓN DE LA HOSPITALIZACIÓN")
        print("-" * 45)
        print(f"🆔 ID: {hospitalizacion.id}")
        print(f"🏠 Habitación: {hospitalizacion.numero_habitacion}")
        print(f"🏥 Tipo de habitación: {hospitalizacion.tipo_habitacion}")
        print(f"🏥 Tipo de cuidado: {hospitalizacion.tipo_cuidado}")
        print(f"📝 Descripción: {hospitalizacion.descripcion}")
        print(f"📅 Fecha de inicio: {hospitalizacion.fecha_inicio}")
        if hospitalizacion.fecha_fin:
            print(f"📅 Fecha de fin: {hospitalizacion.fecha_fin}")
        print(f"📊 Estado: {hospitalizacion.estado}")
        print(f"📅 Registrada: {hospitalizacion.created_at}")
