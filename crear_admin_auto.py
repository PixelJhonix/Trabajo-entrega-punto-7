"""
Script automático para crear el usuario administrador inicial del sistema
Crea un admin con valores por defecto si no existe ninguno
"""
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.config import SessionLocal
from crud.usuario_crud import UsuarioCRUD
from auth.security import PasswordManager


def crear_admin_automatico():
    """Crear usuario administrador inicial automáticamente"""
    db = SessionLocal()
    try:
        usuario_crud = UsuarioCRUD(db)
        
        # Verificar si ya existe un admin con nombre_usuario 'admin'
        admin_existente = usuario_crud.obtener_usuario_por_nombre_usuario("admin")
        
        if admin_existente:
            if admin_existente.es_admin:
                print(f"✓ El usuario administrador 'admin' ya existe.")
                print(f"  Email: {admin_existente.email}")
                print(f"  ID: {admin_existente.id}")
                return admin_existente
            else:
                # Actualizar a admin si no lo es
                admin_existente.es_admin = True
                admin_existente.activo = True
                db.commit()
                db.refresh(admin_existente)
                print(f"✓ Usuario 'admin' actualizado a administrador.")
                print(f"  Email: {admin_existente.email}")
                print(f"  ID: {admin_existente.id}")
                return admin_existente
        
        # Crear nuevo admin con valores por defecto
        print("Creando usuario administrador...")
        
        # Generar contraseña segura
        contraseña = PasswordManager.generate_secure_password(12)
        
        admin = usuario_crud.crear_usuario(
            nombre="Administrador del Sistema",
            nombre_usuario="admin",
            email="admin@hospital.com",
            contraseña=contraseña,
            telefono=None,
            es_admin=True
        )
        
        print("\n" + "="*60)
        print("✓ USUARIO ADMINISTRADOR CREADO EXITOSAMENTE")
        print("="*60)
        print(f"Nombre: {admin.nombre}")
        print(f"Usuario: {admin.nombre_usuario}")
        print(f"Email: {admin.email}")
        print(f"ID: {admin.id}")
        print(f"\nCONTRASEÑA: {contraseña}")
        print("\n⚠️  IMPORTANTE: Guarde esta contraseña de forma segura.")
        print("   Puede cambiarla después de iniciar sesión.")
        print("="*60)
        
        return admin
            
    except ValueError as e:
        print(f"\n❌ Error de validación: {e}")
        return None
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        db.close()


if __name__ == "__main__":
    crear_admin_automatico()






