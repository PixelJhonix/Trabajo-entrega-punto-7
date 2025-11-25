"""
Script para agregar la columna fecha_nacimiento a la tabla tbl_medicos
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


def agregar_fecha_nacimiento():
    """Agregar columna fecha_nacimiento a tbl_medicos"""
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            tabla = "tbl_medicos"
            columna = "fecha_nacimiento"
            
            print(f"\nProcesando tabla: {tabla}")

            if not verificar_columna_existe(conn, tabla, columna):
                print(f"  Agregando {columna} a {tabla}...")
                conn.execute(
                    text(
                        f"""
                        ALTER TABLE {tabla}
                        ADD COLUMN {columna} DATE
                        """
                    )
                )
                print(f"  ✅ {columna} agregada exitosamente a {tabla}")
            else:
                print(f"  ℹ️  {columna} ya existe en {tabla}")

            trans.commit()
            print("\n✅ Proceso completado exitosamente")
        except Exception as e:
            trans.rollback()
            print(f"\n❌ Error al agregar columna: {e}")
            raise


if __name__ == "__main__":
    print("=" * 60)
    print("AGREGANDO COLUMNA fecha_nacimiento A tbl_medicos")
    print("=" * 60)
    print(f"Fecha: {datetime.now()}")
    print(f"Base de datos: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}")
    print("=" * 60)

    try:
        agregar_fecha_nacimiento()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)




