"""
Script para verificar el usuario admin y probar autenticación
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.config import SessionLocal
from crud.usuario_crud import UsuarioCRUD
from auth.security import PasswordManager


def verificar_admin():
    """Verificar usuario admin y probar autenticación"""
    db = SessionLocal()
    try:
        usuario_crud = UsuarioCRUD(db)
        
        # Buscar usuario admin
        admin = usuario_crud.obtener_usuario_por_nombre_usuario("admin")
        
        if not admin:
            print("❌ No se encontró el usuario 'admin'")
            # Buscar por email
            admin = usuario_crud.obtener_usuario_por_email("admin@hospital.com")
            if admin:
                print("✓ Usuario encontrado por email")
        
        if not admin:
            print("❌ No se encontró ningún usuario admin")
            return
        
        print("\n" + "="*60)
        print("INFORMACIÓN DEL USUARIO ADMIN")
        print("="*60)
        print(f"ID: {admin.id}")
        print(f"Nombre: {admin.nombre}")
        print(f"Nombre Usuario: {admin.nombre_usuario}")
        print(f"Email: {admin.email}")
        print(f"Es Admin: {admin.es_admin}")
        print(f"Activo: {admin.activo}")
        print(f"Hash Contraseña: {admin.contraseña_hash[:50]}...")
        print("="*60)
        
        # Probar autenticación con diferentes credenciales
        print("\nProbando autenticación...")
        
        # La contraseña que generamos
        contraseñas_prueba = [
            "ax,+5B]cL%=V",  # La que generamos
            "admin123",      # Por si acaso
        ]
        
        for pwd in contraseñas_prueba:
            print(f"\nProbando contraseña: {pwd}")
            es_valida = PasswordManager.verify_password(pwd, admin.contraseña_hash)
            print(f"  Resultado: {'✓ VÁLIDA' if es_valida else '❌ INVÁLIDA'}")
            
            if es_valida:
                # Probar autenticación completa
                usuario_autenticado = usuario_crud.autenticar_usuario("admin", pwd)
                if usuario_autenticado:
                    print(f"  ✓ Autenticación exitosa con nombre_usuario='admin'")
                else:
                    print(f"  ❌ Autenticación falló con nombre_usuario='admin'")
                
                usuario_autenticado = usuario_crud.autenticar_usuario("admin@hospital.com", pwd)
                if usuario_autenticado:
                    print(f"  ✓ Autenticación exitosa con email='admin@hospital.com'")
                else:
                    print(f"  ❌ Autenticación falló con email='admin@hospital.com'")
                break
        
        print("\n" + "="*60)
        print("RECOMENDACIONES:")
        print("="*60)
        print("Si ninguna contraseña funcionó, ejecuta crear_admin_auto.py")
        print("para crear un nuevo admin con contraseña conocida.")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    verificar_admin()






