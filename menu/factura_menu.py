"""Menú de gestión de facturas."""

import os
from decimal import Decimal
from uuid import UUID

from crud.factura_crud import FacturaCRUD


class FacturaMenu:
    """Menú para gestión de facturas."""

    def __init__(self, db, auth_service):
        self.db = db
        self.auth_service = auth_service
        self.factura_crud = FacturaCRUD(db)

    def limpiar_pantalla(self):
        """Limpiar la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_titulo(self):
        """Mostrar título del módulo."""
        print("FACTURA GESTIÓN DE FACTURAS")
        print("=" * 40)

    def mostrar_menu(self):
        """Mostrar menú de facturas."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                print("\nOPCIONES DISPONIBLES")
                print("-" * 25)
                print("1. Crear Nueva Factura")
                print("2. Buscar Factura")
                print("3. Listar Facturas")
                print("4. Actualizar Factura")
                print("5. 💳 Marcar como Pagada")
                print("6. Cancelar Factura")
                print("0. Volver al Menú Principal")

                opcion = input("\nSeleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.crear_factura()
                elif opcion == "2":
                    self.buscar_factura()
                elif opcion == "3":
                    self.listar_facturas()
                elif opcion == "4":
                    self.actualizar_factura()
                elif opcion == "5":
                    self.marcar_como_pagada()
                elif opcion == "6":
                    self.cancelar_factura()
                else:
                    print("Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                input("Presione Enter para continuar...")

    def crear_factura(self):
        """Crear una nueva factura."""
        self.limpiar_pantalla()
        print("CREAR NUEVA FACTURA")
        print("-" * 35)

        try:
            paciente_id = input("del paciente: ").strip()
            if not paciente_id:
                print("El del paciente es obligatorio")
                input("Presione Enter para continuar...")
                return

            numero_factura = input("📄 Número de factura: ").strip()
            if not numero_factura:
                print("El número de factura es obligatorio")
                input("Presione Enter para continuar...")
                return

            fecha_emision = input("Fecha de emisión (YYYY-MM-DD): ").strip()
            if not fecha_emision:
                print("La fecha de emisión es obligatoria")
                input("Presione Enter para continuar...")
                return

            fecha_limite_pago = input("Fecha límite de pago (YYYY-MM-DD): ").strip()
            if not fecha_limite_pago:
                print("La fecha límite de pago es obligatoria")
                input("Presione Enter para continuar...")
                return

            total = input("💰 Total de la factura: ").strip()
            if not total:
                print("El total es obligatorio")
                input("Presione Enter para continuar...")
                return

            try:
                total_decimal = Decimal(total)
            except:
                print("El total debe ser un número válido")
                input("Presione Enter para continuar...")
                return

            metodo_pago = input("💳 Método de pago (opcional): ").strip()
            if not metodo_pago:
                metodo_pago = None

            usuario_actual = self.auth_service.usuario_actual
            if not usuario_actual:
                print("No hay usuario autenticado")
                input("Presione Enter para continuar...")
                return

            factura = self.factura_crud.crear_factura(
                paciente_id=UUID(paciente_id),
                numero_factura=numero_factura,
                fecha_emision=fecha_emision,
                fecha_limite_pago=fecha_limite_pago,
                total=total_decimal,
                id_usuario_creacion=usuario_actual.id,
                metodo_pago=metodo_pago,
            )

            print(f"\nFactura creada exitosamente!")
            print(f"ID: {factura.id}")
            print(f"📄 Número: {factura.numero_factura}")
            print(f"💰 Total: ${factura.total}")
            print(f"Estado: {factura.estado}")

        except ValueError as e:
            print(f"Error de validación: {e}")
        except Exception as e:
            print(f"Error: {e}")

        input("\nPresione Enter para continuar...")

    def buscar_factura(self):
        """Buscar una factura."""
        self.limpiar_pantalla()
        print("BUSCAR FACTURA")
        print("-" * 25)

        try:
            print("Opciones de búsqueda:")
            print("1. Por ID")
            print("2. Por número de factura")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                factura_id = input("de la factura: ").strip()
                if not factura_id:
                    print("El es obligatorio")
                    input("Presione Enter para continuar...")
                    return

                factura = self.factura_crud.obtener_factura(UUID(factura_id))
                if factura:
                    self.mostrar_factura(factura)
                else:
                    print("Factura no encontrada")

            elif opcion == "2":
                numero_factura = input("📄 Número de factura: ").strip()
                if not numero_factura:
                    print("El número de factura es obligatorio")
                    input("Presione Enter para continuar...")
                    return

                factura = self.factura_crud.obtener_factura_por_numero(numero_factura)
                if factura:
                    self.mostrar_factura(factura)
                else:
                    print("Factura no encontrada")

            else:
                print("Opción inválida")

        except ValueError as e:
            print(f"Error de validación: {e}")
        except Exception as e:
            print(f"Error: {e}")

        input("\nPresione Enter para continuar...")

    def listar_facturas(self):
        """Listar todas las facturas."""
        self.limpiar_pantalla()
        print("LISTA DE FACTURAS")
        print("-" * 25)

        try:
            facturas = self.factura_crud.obtener_facturas()
            if facturas:
                print(f"\nTotal de facturas: {len(facturas)}")
                print("-" * 80)
                for i, factura in enumerate(facturas, 1):
                    print(f"{i:2d}. Factura #{factura.numero_factura}")
                    print(f"     💰 Total: ${factura.total}")
                    print(f"     Estado: {factura.estado}")
                    print(f"     Emisión: {factura.fecha_emision}")
                    print(f"     Límite: {factura.fecha_limite_pago}")
                    print(f"     ID: {factura.id}")
                    print("-" * 80)
            else:
                print(" No hay facturas registradas")

        except Exception as e:
            print(f"Error: {e}")

        input("\nPresione Enter para continuar...")

    def actualizar_factura(self):
        """Actualizar una factura."""
        self.limpiar_pantalla()
        print("ACTUALIZAR FACTURA")
        print("-" * 30)

        try:
            factura_id = input("de la factura: ").strip()
            if not factura_id:
                print("El es obligatorio")
                input("Presione Enter para continuar...")
                return

            factura = self.factura_crud.obtener_factura(UUID(factura_id))
            if not factura:
                print("Factura no encontrada")
                input("Presione Enter para continuar...")
                return

            print(f"\n📄 Factura: {factura.numero_factura}")
            print("Deje en blanco para mantener el valor actual\n")

            campos = {}

            nuevo_estado = input(f"Estado [{factura.estado}]: ").strip()
            if nuevo_estado:
                campos["estado"] = nuevo_estado

            nuevo_metodo_pago = input(
                f"💳 Método de pago [{factura.metodo_pago or 'No especificado'}]: "
            ).strip()
            if nuevo_metodo_pago:
                campos["metodo_pago"] = nuevo_metodo_pago

            if campos:
                usuario_actual = self.auth_service.usuario_actual
                factura_actualizada = self.factura_crud.actualizar_factura(
                    UUID(factura_id), usuario_actual.id, **campos
                )
                print(f"\nFactura actualizada exitosamente!")
            else:
                print(" No se realizaron cambios")

        except ValueError as e:
            print(f"Error de validación: {e}")
        except Exception as e:
            print(f"Error: {e}")

        input("\nPresione Enter para continuar...")

    def marcar_como_pagada(self):
        """Marcar una factura como pagada."""
        self.limpiar_pantalla()
        print("💳 MARCAR COMO PAGADA")
        print("-" * 30)

        try:
            factura_id = input("de la factura: ").strip()
            if not factura_id:
                print("El es obligatorio")
                input("Presione Enter para continuar...")
                return

            metodo_pago = input("💳 Método de pago utilizado: ").strip()
            if not metodo_pago:
                print("El método de pago es obligatorio")
                input("Presione Enter para continuar...")
                return

            usuario_actual = self.auth_service.usuario_actual
            if self.factura_crud.pagar_factura(
                UUID(factura_id), metodo_pago, usuario_actual.id
            ):
                print("Factura marcada como pagada exitosamente")
            else:
                print("Error al marcar la factura como pagada")

        except ValueError as e:
            print(f"Error de validación: {e}")
        except Exception as e:
            print(f"Error: {e}")

        input("\nPresione Enter para continuar...")

    def cancelar_factura(self):
        """Cancelar una factura."""
        self.limpiar_pantalla()
        print("CANCELAR FACTURA")
        print("-" * 25)

        try:
            factura_id = input("de la factura: ").strip()
            if not factura_id:
                print("El es obligatorio")
                input("Presione Enter para continuar...")
                return

            factura = self.factura_crud.obtener_factura(UUID(factura_id))
            if not factura:
                print("Factura no encontrada")
                input("Presione Enter para continuar...")
                return

            print(f"\n📄 Factura: {factura.numero_factura}")
            print(f"💰 Total: ${factura.total}")
            print(f"Estado: {factura.estado}")

            confirmar = (
                input("\n¿Está seguro de cancelar esta factura? (s/N): ")
                .strip()
                .lower()
            )
            if confirmar in ["s", "si", "sí", "y", "yes"]:
                usuario_actual = self.auth_service.usuario_actual
                if self.factura_crud.cancelar_factura(
                    UUID(factura_id), usuario_actual.id
                ):
                    print("Factura cancelada exitosamente")
                else:
                    print("Error al cancelar la factura")
            else:
                print(" Operación cancelada")

        except ValueError as e:
            print(f"Error de validación: {e}")
        except Exception as e:
            print(f"Error: {e}")

        input("\nPresione Enter para continuar...")

    def mostrar_factura(self, factura):
        """Mostrar información de una factura."""
        print(f"\nFACTURA INFORMACIÓN DE LA FACTURA")
        print("-" * 35)
        print(f"ID: {factura.id}")
        print(f"📄 Número: {factura.numero_factura}")
        print(f"💰 Total: ${factura.total}")
        print(f"Estado: {factura.estado}")
        print(f"Fecha de emisión: {factura.fecha_emision}")
        print(f"Fecha límite: {factura.fecha_limite_pago}")
        if factura.metodo_pago:
            print(f"💳 Método de pago: {factura.metodo_pago}")
        print(f"Creada: {factura.created_at}")
