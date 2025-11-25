"""
Script para agregar las columnas faltantes a la tabla tbl_medicos
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


def agregar_columnas_faltantes():
    """Agregar columnas faltantes a tbl_medicos"""
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            tabla = "tbl_medicos"
            
            print(f"\nProcesando tabla: {tabla}")

            # Agregar consultorio
            if not verificar_columna_existe(conn, tabla, "consultorio"):
                print(f"  Agregando consultorio a {tabla}...")
                conn.execute(
                    text(
                        f"""
                        ALTER TABLE {tabla}
                        ADD COLUMN consultorio VARCHAR(50)
                        """
                    )
                )
                print(f"  ✅ consultorio agregada exitosamente")
            else:
                print(f"  ℹ️  consultorio ya existe")

            # Agregar direccion
            if not verificar_columna_existe(conn, tabla, "direccion"):
                print(f"  Agregando direccion a {tabla}...")
                conn.execute(
                    text(
                        f"""
                        ALTER TABLE {tabla}
                        ADD COLUMN direccion VARCHAR(255)
                        """
                    )
                )
                print(f"  ✅ direccion agregada exitosamente")
            else:
                print(f"  ℹ️  direccion ya existe")

            # Hacer fecha_nacimiento NOT NULL si tiene datos, o dejarla nullable
            # Por ahora la dejamos nullable para no romper registros existentes

            trans.commit()
            print("\n✅ Proceso completado exitosamente")
        except Exception as e:
            trans.rollback()
            print(f"\n❌ Error al agregar columnas: {e}")
            raise


if __name__ == "__main__":
    print("=" * 60)
    print("AGREGANDO COLUMNAS FALTANTES A tbl_medicos")
    print("=" * 60)
    print(f"Fecha: {datetime.now()}")
    print(f"Base de datos: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}")
    print("=" * 60)

    try:
        agregar_columnas_faltantes()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)




