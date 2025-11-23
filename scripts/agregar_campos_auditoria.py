"""
Script para agregar campos de auditoría a las tablas existentes
Ejecutar este script si las tablas ya existen pero no tienen los campos de auditoría
"""

import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL no está configurada en las variables de entorno")
    sys.exit(1)

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"sslmode": "require"},
)

tablas = [
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
]


def verificar_columna_existe(conn, tabla, columna):
    """Verificar si una columna existe en una tabla"""
    query = text(
        """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = :tabla AND column_name = :columna
        """
    )
    result = conn.execute(query, {"tabla": tabla, "columna": columna})
    return result.fetchone() is not None


def agregar_campos_auditoria():
    """Agregar campos de auditoría a todas las tablas"""
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            for tabla in tablas:
                print(f"\nProcesando tabla: {tabla}")

                if not verificar_columna_existe(conn, tabla, "fecha_creacion"):
                    print(f"  Agregando fecha_creacion a {tabla}...")
                    conn.execute(
                        text(
                            f"""
                            ALTER TABLE {tabla}
                            ADD COLUMN fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                            """
                        )
                    )
                else:
                    print(f"  fecha_creacion ya existe en {tabla}")

                if not verificar_columna_existe(conn, tabla, "fecha_actualizacion"):
                    print(f"  Agregando fecha_actualizacion a {tabla}...")
                    conn.execute(
                        text(
                            f"""
                            ALTER TABLE {tabla}
                            ADD COLUMN fecha_actualizacion TIMESTAMP WITH TIME ZONE
                            """
                        )
                    )
                else:
                    print(f"  fecha_actualizacion ya existe en {tabla}")

                if not verificar_columna_existe(conn, tabla, "id_usuario_creacion"):
                    print(f"  Agregando id_usuario_creacion a {tabla}...")
                    conn.execute(
                        text(
                            f"""
                            ALTER TABLE {tabla}
                            ADD COLUMN id_usuario_creacion UUID
                            """
                        )
                    )
                else:
                    print(f"  id_usuario_creacion ya existe en {tabla}")

                if not verificar_columna_existe(conn, tabla, "id_usuario_edicion"):
                    print(f"  Agregando id_usuario_edicion a {tabla}...")
                    conn.execute(
                        text(
                            f"""
                            ALTER TABLE {tabla}
                            ADD COLUMN id_usuario_edicion UUID
                            """
                        )
                    )
                else:
                    print(f"  id_usuario_edicion ya existe en {tabla}")

            trans.commit()
            print("\n✅ Campos de auditoría agregados exitosamente a todas las tablas")
        except Exception as e:
            trans.rollback()
            print(f"\n❌ Error al agregar campos de auditoría: {e}")
            raise


if __name__ == "__main__":
    print("=" * 60)
    print("AGREGANDO CAMPOS DE AUDITORÍA A LAS TABLAS")
    print("=" * 60)
    print(f"Fecha: {datetime.now()}")
    print(f"Base de datos: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}")
    print("=" * 60)

    try:
        agregar_campos_auditoria()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

