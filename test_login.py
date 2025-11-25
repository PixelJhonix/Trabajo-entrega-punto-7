"""
Script para probar el login del usuario administrador
"""
import requests
import json

def test_login():
    url = "http://localhost:8000/api/auth/login"
    
    # Credenciales del admin creado
    data = {
        "nombre_usuario": "admin",
        "contraseña": "ax,+5B]cL%=V"
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("="*60)
            print("✓ LOGIN EXITOSO")
            print("="*60)
            print(f"Token: {result.get('access_token', '')[:50]}...")
            print(f"Tipo: {result.get('token_type', '')}")
            print(f"\nUsuario:")
            user = result.get('user', {})
            print(f"  ID: {user.get('id', '')}")
            print(f"  Nombre: {user.get('nombre', '')}")
            print(f"  Email: {user.get('email', '')}")
            print(f"  Usuario: {user.get('nombre_usuario', '')}")
            print(f"  Es Admin: {user.get('es_admin', False)}")
            print("="*60)
            return True
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrese de que el backend esté corriendo en http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    test_login()






