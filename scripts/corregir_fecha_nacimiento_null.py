"""
Script para corregir registros con fecha_nacimiento NULL en tbl_medicos
"""

import os
import sys
from datetime import date, datetime

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


def corregir_fecha_nacimiento_null():
    """Corregir registros con fecha_nacimiento NULL"""
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            # Primero, hacer la columna nullable temporalmente
            print("\n1. Haciendo fecha_nacimiento nullable...")
            conn.execute(
                text(
                    """
                    ALTER TABLE tbl_medicos
                    ALTER COLUMN fecha_nacimiento DROP NOT NULL
                    """
                )
            )
            print("   ✅ Columna ahora es nullable")
            
            # Actualizar registros con NULL a una fecha por defecto (ej: 1970-01-01)
            print("\n2. Actualizando registros con fecha_nacimiento NULL...")
            result = conn.execute(
                text(
                    """
                    UPDATE tbl_medicos
                    SET fecha_nacimiento = '1970-01-01'::date
                    WHERE fecha_nacimiento IS NULL
                    """
                )
            )
            print(f"   ✅ {result.rowcount} registros actualizados")
            
            # Opcional: Volver a hacer NOT NULL si quieres
            # Por ahora la dejamos nullable para evitar problemas futuros
            
            trans.commit()
            print("\n✅ Proceso completado exitosamente")
        except Exception as e:
            trans.rollback()
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    print("=" * 60)
    print("CORRIGIENDO fecha_nacimiento NULL EN tbl_medicos")
    print("=" * 60)
    print(f"Fecha: {datetime.now()}")
    print(f"Base de datos: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}")
    print("=" * 60)

    try:
        corregir_fecha_nacimiento_null()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)




