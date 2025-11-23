"""
Script para verificar la estructura completa de la tabla tbl_medicos
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


def verificar_estructura_tabla():
    """Verificar todas las columnas de la tabla tbl_medicos"""
    with engine.connect() as conn:
        query = text(
            """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'tbl_medicos'
            ORDER BY ordinal_position
            """
        )
        result = conn.execute(query)
        columns = result.fetchall()
        
        print("\n" + "=" * 80)
        print("ESTRUCTURA DE LA TABLA tbl_medicos")
        print("=" * 80)
        print(f"{'Columna':<30} {'Tipo':<25} {'Nullable':<10} {'Default'}")
        print("-" * 80)
        
        for col in columns:
            col_name = col[0]
            data_type = col[1]
            is_nullable = col[2]
            default = col[3] or ''
            print(f"{col_name:<30} {data_type:<25} {is_nullable:<10} {default}")
        
        print("=" * 80)
        
        # Verificar columnas esperadas
        columnas_esperadas = [
            'id', 'nombre', 'apellido', 'email', 'telefono', 'especialidad',
            'numero_licencia', 'fecha_nacimiento', 'consultorio', 'direccion',
            'activo', 'fecha_creacion', 'fecha_actualizacion',
            'id_usuario_creacion', 'id_usuario_edicion'
        ]
        
        columnas_existentes = [col[0] for col in columns]
        
        print("\nVERIFICACIÓN DE COLUMNAS ESPERADAS:")
        print("-" * 80)
        faltantes = []
        for col_esperada in columnas_esperadas:
            if col_esperada in columnas_existentes:
                print(f"✅ {col_esperada}")
            else:
                print(f"❌ {col_esperada} - FALTANTE")
                faltantes.append(col_esperada)
        
        if faltantes:
            print(f"\n⚠️  Columnas faltantes: {', '.join(faltantes)}")
        else:
            print("\n✅ Todas las columnas esperadas están presentes")


if __name__ == "__main__":
    print("=" * 80)
    print("VERIFICANDO ESTRUCTURA DE tbl_medicos")
    print("=" * 80)
    print(f"Fecha: {datetime.now()}")
    print(f"Base de datos: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}")
    
    try:
        verificar_estructura_tabla()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

