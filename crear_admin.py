"""
Script para crear el usuario administrador inicial del sistema
"""
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.config import SessionLocal
from crud.usuario_crud import UsuarioCRUD
from auth.security import PasswordManager


def crear_admin():
    """Crear usuario administrador inicial"""
    db = SessionLocal()
    try:
        usuario_crud = UsuarioCRUD(db)
        
        # Verificar si ya existe un admin
        admins = usuario_crud.obtener_usuarios_admin()
        if admins:
            print(f"Ya existe {len(admins)} usuario(s) administrador(es) en el sistema:")
            for admin in admins:
                print(f"  - {admin.nombre_usuario} ({admin.email})")
            respuesta = input("\n¿Desea crear otro admin? (s/n): ").strip().lower()
            if respuesta != 's':
                print("Operación cancelada.")
                return
        
        # Verificar si ya existe el usuario 'admin'
        admin_existente = usuario_crud.obtener_usuario_por_nombre_usuario("admin")
        if admin_existente:
            print("El usuario 'admin' ya existe.")
            respuesta = input("¿Desea actualizarlo a administrador? (s/n): ").strip().lower()
            if respuesta == 's':
                admin_existente.es_admin = True
                admin_existente.activo = True
                db.commit()
                print(f"Usuario 'admin' actualizado a administrador exitosamente.")
                print(f"ID: {admin_existente.id}")
                print(f"Email: {admin_existente.email}")
                return
            else:
                print("Operación cancelada.")
                return
        
        print("\n=== Crear Usuario Administrador ===")
        print("Ingrese los datos del administrador:")
        print("(Presione Enter para usar valores por defecto)")
        
        nombre = input("Nombre completo [Administrador del Sistema]: ").strip()
        if not nombre:
            nombre = "Administrador del Sistema"
        
        nombre_usuario = input("Nombre de usuario [admin]: ").strip()
        if not nombre_usuario:
            nombre_usuario = "admin"
        
        email = input("Email [admin@hospital.com]: ").strip()
        if not email:
            email = "admin@hospital.com"
        
        telefono = input("Teléfono (opcional): ").strip()
        if not telefono:
            telefono = None
        
        # Generar contraseña segura o pedirla al usuario
        print("\nOpciones de contraseña:")
        print("1. Generar contraseña segura automáticamente")
        print("2. Ingresar contraseña manualmente")
        opcion = input("Seleccione opción [1]: ").strip()
        
        if opcion == "2":
            while True:
                contraseña = input("Contraseña (mínimo 8 caracteres, con mayúscula, minúscula, número y carácter especial): ").strip()
                es_valida, mensaje = PasswordManager.validate_password_strength(contraseña)
                if es_valida:
                    break
                print(f"Error: {mensaje}")
                respuesta = input("¿Desea intentar de nuevo? (s/n): ").strip().lower()
                if respuesta != 's':
                    print("Operación cancelada.")
                    return
        else:
            contraseña = PasswordManager.generate_secure_password(12)
            print(f"\nContraseña generada: {contraseña}")
            print("IMPORTANTE: Guarde esta contraseña de forma segura.")
        
        # Crear el usuario admin
        try:
            admin = usuario_crud.crear_usuario(
                nombre=nombre,
                nombre_usuario=nombre_usuario,
                email=email,
                contraseña=contraseña,
                telefono=telefono,
                es_admin=True
            )
            
            print("\n" + "="*50)
            print("✓ Usuario administrador creado exitosamente!")
            print("="*50)
            print(f"ID: {admin.id}")
            print(f"Nombre: {admin.nombre}")
            print(f"Usuario: {admin.nombre_usuario}")
            print(f"Email: {admin.email}")
            print(f"Teléfono: {admin.telefono or 'N/A'}")
            print(f"Es Admin: {admin.es_admin}")
            print(f"Activo: {admin.activo}")
            if opcion != "2":
                print(f"\nContraseña: {contraseña}")
                print("⚠️  IMPORTANTE: Cambie esta contraseña en su primer inicio de sesión")
            print("="*50)
            
        except ValueError as e:
            print(f"\n❌ Error al crear usuario: {e}")
            return
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            return
            
    except Exception as e:
        print(f"\n❌ Error de conexión a la base de datos: {e}")
        return
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  CREAR USUARIO ADMINISTRADOR")
    print("  Sistema Hospitalario")
    print("="*50 + "\n")
    
    crear_admin()
    
    print("\nPresione Enter para salir...")
    input()




