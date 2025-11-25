"""
Script para crear un usuario admin con contraseña simple
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.config import SessionLocal
from crud.usuario_crud import UsuarioCRUD


def crear_admin_simple():
    """Crear usuario administrador con contraseña simple"""
    db = SessionLocal()
    try:
        usuario_crud = UsuarioCRUD(db)
        
        # Verificar si ya existe
        admin_existente = usuario_crud.obtener_usuario_por_nombre_usuario("admin")
        
        if admin_existente:
            print("El usuario 'admin' ya existe.")
            print("Actualizando contraseña a 'Admin123!@#'...")
            
            # Actualizar contraseña
            usuario_crud.actualizar_usuario(
                admin_existente.id,
                contraseña="Admin123!@#"
            )
            print("✓ Contraseña actualizada exitosamente")
        else:
            # Crear nuevo admin
            admin = usuario_crud.crear_usuario(
                nombre="Administrador del Sistema",
                nombre_usuario="admin",
                email="admin@hospital.com",
                contraseña="Admin123!@#",
                telefono=None,
                es_admin=True
            )
            print("✓ Usuario administrador creado exitosamente")
        
        print("\n" + "="*60)
        print("CREDENCIALES DE ACCESO")
        print("="*60)
        print("Usuario: admin")
        print("Contraseña: Admin123!@#")
        print("Email: admin@hospital.com")
        print("="*60)
        print("\n⚠️  IMPORTANTE: Cambie esta contraseña después del primer login")
        print("="*60)
        
    except ValueError as e:
        print(f"❌ Error de validación: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    crear_admin_simple()






