#!/usr/bin/env python3
"""
Script para eliminar tablas duplicadas AUTOMÁTICAMENTE (sin confirmación).
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError


# Colores para la salida
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def get_database_url():
    """Obtener la URL de conexión a la base de datos."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)

        from database.config import DATABASE_URL

        if DATABASE_URL:
            return DATABASE_URL
    except Exception as e:
        print_warning(f"No se pudo cargar desde config.py: {e}")

    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url

    try:
        from dotenv import load_dotenv

        load_dotenv()
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            return db_url
    except ImportError:
        pass

    print_error("No se encontró DATABASE_URL")
    sys.exit(1)


def get_tables_to_keep():
    """Lista de tablas que deben mantenerse."""
    return {
        "tbl_usuarios",
        "tbl_pacientes",
        "tbl_medicos",
        "tbl_enfermeras",
        "tbl_citas",
        "tbl_hospitalizaciones",
        "tbl_historiales_medicos",
        "tbl_historial_entradas",
        "tbl_facturas",
        "tbl_factura_detalles",
        "alembic_version",
    }


def list_all_tables(engine):
    """Listar todas las tablas en la base de datos."""
    inspector = inspect(engine)
    return inspector.get_table_names()


def identify_tables_to_delete(all_tables, tables_to_keep):
    """Identificar qué tablas deben eliminarse."""
    tables_to_delete = []

    for table in all_tables:
        if table.startswith("tbl_"):
            continue
        if table in tables_to_keep:
            continue
        tables_to_delete.append(table)

    return sorted(tables_to_delete)


def main():
    print_header("Script de Limpieza de Tablas Duplicadas (AUTOMÁTICO)")

    print("Conectando a la base de datos...")
    try:
        db_url = get_database_url()
        engine = create_engine(db_url)

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print_success("Conexión establecida")
    except Exception as e:
        print_error(f"Error al conectar: {e}")
        sys.exit(1)

    print("\nObteniendo lista de tablas...")
    all_tables = list_all_tables(engine)
    print_success(f"Se encontraron {len(all_tables)} tablas en total")

    tables_to_keep = get_tables_to_keep()
    tables_to_delete = identify_tables_to_delete(all_tables, tables_to_keep)

    print_header("Resumen de Tablas")

    print(f"\n{Colors.BOLD}Tablas que se MANTENDRÁN:{Colors.RESET}")
    tables_to_keep_found = [
        t for t in all_tables if t.startswith("tbl_") or t in tables_to_keep
    ]
    for table in sorted(tables_to_keep_found):
        print(f"  {Colors.GREEN}✓ {table}{Colors.RESET}")

    if tables_to_delete:
        print(f"\n{Colors.BOLD}Tablas que se ELIMINARÁN:{Colors.RESET}")
        for table in tables_to_delete:
            print(f"  {Colors.RED}✗ {table}{Colors.RESET}")

        print_header("Eliminando Tablas")
        print_warning(f"Eliminando {len(tables_to_delete)} tabla(s) automáticamente...")

        deleted_count = 0
        errors = []

        with engine.begin() as conn:
            for table in tables_to_delete:
                try:
                    print(f"Eliminando tabla: {table}...", end=" ")
                    conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                    print_success(f"Tabla '{table}' eliminada")
                    deleted_count += 1
                except SQLAlchemyError as e:
                    error_msg = f"Error al eliminar '{table}': {e}"
                    print_error(error_msg)
                    errors.append(error_msg)

        print_header("Resumen Final")
        print_success(f"Tablas eliminadas: {deleted_count}")

        if errors:
            print_warning(f"Errores encontrados: {len(errors)}")
            for error in errors:
                print(f"  {Colors.RED}{error}{Colors.RESET}")
    else:
        print(f"\n{Colors.GREEN}No hay tablas duplicadas para eliminar.{Colors.RESET}")

    print("\nTablas restantes en la base de datos:")
    remaining_tables = list_all_tables(engine)
    for table in sorted(remaining_tables):
        if table.startswith("tbl_"):
            print(f"  {Colors.GREEN}✓ {table}{Colors.RESET}")
        elif table == "alembic_version":
            print(f"  {Colors.BLUE}→ {table} (sistema){Colors.RESET}")
        else:
            print(f"  {Colors.YELLOW}? {table}{Colors.RESET}")

    print_success("Proceso completado")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
