"""
Script para probar el login directamente con HTTP
"""
import urllib.request
import urllib.parse
import json

def test_login_http():
    url = "http://localhost:8000/api/auth/login"
    
    # Datos del login
    data = {
        "nombre_usuario": "admin",
        "contraseña": "ax,+5B]cL%=V"
    }
    
    try:
        # Preparar la petición
        data_json = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data_json,
            headers={'Content-Type': 'application/json'}
        )
        
        # Enviar petición
        print(f"Enviando petición POST a {url}")
        print(f"Datos: {json.dumps(data, indent=2)}")
        print("-" * 60)
        
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_data = json.loads(response.read().decode('utf-8'))
            
            print(f"✓ Status Code: {status_code}")
            print(f"✓ Respuesta:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            
            if status_code == 200:
                print("\n" + "="*60)
                print("✓ LOGIN EXITOSO")
                print("="*60)
                return True
            else:
                print(f"\n❌ Error: Status {status_code}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"❌ Error HTTP: {e.code}")
        error_body = e.read().decode('utf-8')
        print(f"Respuesta: {error_body}")
        try:
            error_json = json.loads(error_body)
            print(f"Detalle: {json.dumps(error_json, indent=2, ensure_ascii=False)}")
        except:
            print(f"Error no es JSON: {error_body}")
        return False
    except urllib.error.URLError as e:
        print(f"❌ Error de conexión: {e}")
        print("   Asegúrese de que el backend esté corriendo en http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  PRUEBA DE LOGIN HTTP")
    print("="*60 + "\n")
    test_login_http()




