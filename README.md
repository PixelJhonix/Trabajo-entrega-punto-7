# Sistema de Gestión Hospitalaria - Punto 7

## Descripción
Sistema de gestión hospitalaria desarrollado en Python que implementa un sistema de registro de pacientes, médicos y enfermeras. El proyecto demuestra conceptos avanzados de Programación Orientada a Objetos (POO) incluyendo herencia, polimorfismo y encapsulación.

## Características Principales

- **Registro de Personas**: Sistema unificado para pacientes, médicos y enfermeras
- **Herencia de Clases**: Estructura jerárquica con clase base `Persona`
- **Encapsulación**: Atributos privados con métodos públicos para acceso
- **Polimorfismo**: Métodos `mostrardatos()` personalizados para cada tipo
- **Métodos de Clase**: Funciones de registro integradas en cada clase
- **Interfaz de Consola**: Menú interactivo para gestión del sistema

## Instalación

### Prerrequisitos
- **Python 3.8+** instalado en tu sistema
- **Git** para clonar el repositorio
- **Editor de código** (VS Code, PyCharm, Cursor, etc.)

### Extensiones Recomendadas para VS Code/Cursor
- **Python** (Microsoft)
- **Pylance** (Microsoft)
- **Python Indent** (Kevin Rose)
- **Python Docstring Generator** (Nils Werner)
- **GitLens** (Eric Amodio)

## Clonar el Repositorio

```bash
# Clonar desde GitHub
git clone https://github.com/tu-usuario/trabajo-entrega-punto-7.git

# Navegar al directorio del proyecto
cd trabajo-entrega-punto-7
```

## Configuración

### 1. Crear entorno virtual (Recomendado)
```bash
# Crear entorno virtual
py -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
# Este proyecto no requiere dependencias externas
# Solo Python estándar (built-in modules)
```

## Ejecutar el Proyecto

```bash
# Ejecutar el sistema hospitalario
py main.py

# O ejecutar archivos específicos
py persona.py
py paciente.py
py medico.py
py enfermera.py
```

## Estructura del Proyecto

```
trabajo-entrega-punto-7/
├── main.py                 # Archivo principal con menú y lógica
├── persona.py              # Clase base Persona
├── paciente.py             # Clase Paciente (hereda de Persona)
├── medico.py               # Clase Medico (hereda de Persona)
├── enfermera.py            # Clase Enfermera (hereda de Persona)
├── .gitignore              # Archivos a ignorar
└── README.md               # Este archivo
```

## Arquitectura del Sistema

### Clase Base: Persona
```python
class Persona:
    # Atributos comunes: nombre, fecha_nac, telefono, direccion
    # Método: mostrardatos()
```

### Clases Derivadas

#### Paciente
- **Hereda de**: Persona
- **Atributos adicionales**: tipo = "Paciente"
- **Funcionalidad**: Registro de datos personales

#### Medico
- **Hereda de**: Persona
- **Atributos adicionales**: especialidad, tipo = "Médico"
- **Funcionalidad**: Registro de datos personales y especialidad

#### Enfermera
- **Hereda de**: Persona
- **Atributos adicionales**: turno, tipo = "Enfermera"
- **Funcionalidad**: Registro de datos personales y turno

## Uso del Sistema

### Menú Principal
1. **Registrar Paciente** - Crear nuevo paciente
2. **Registrar Médico** - Crear nuevo médico
3. **Registrar Enfermera** - Crear nueva enfermera
4. **Mostrar Todos los Registros** - Ver todos los registros
0. **Salir** - Terminar programa

### Ejemplo de Uso
```python
# El sistema solicita datos interactivamente
# Ejemplo de registro de paciente:
# Nombre: Juan Pérez
# Fecha de nacimiento: 15/03/1990
# Teléfono: 555-0123
# Dirección: Calle Principal 123
```

## Conceptos POO Implementados

### 1. Herencia
- Todas las clases heredan de `Persona`
- Uso de `super().__init__()` para inicialización del padre

### 2. Encapsulación
- Atributos privados con `_` (ej: `_nombre`, `_telefono`)
- Métodos públicos para acceso a datos

### 3. Polimorfismo
- Método `mostrardatos()` personalizado en cada clase
- Comportamiento diferente según el tipo de persona

### 4. Métodos de Clase
- `@classmethod` para funciones de registro
- Cada clase maneja su propio proceso de registro

## Desarrollo

### Flujo de trabajo Git
```bash
# 1. Crear rama para nueva funcionalidad
git checkout -b feature/nueva-funcionalidad

# 2. Hacer cambios y commits
git add .
git commit -m "feat: agregar nueva funcionalidad"

# 3. Subir cambios
git push origin feature/nueva-funcionalidad

# 4. Crear Pull Request en GitHub
# 5. Esperar revisión del compañero (QA)
# 6. Merge después de aprobación
```

### Estándares de código
- **PEP 8** para estilo de código Python
- **Mensajes de commit** descriptivos
- **Documentación** en funciones y clases
- **Type hints** para mejor legibilidad

## Solución de Problemas

### Error común: "Python no se reconoce"
```bash
# Verificar instalación de Python
py --version

# Si no funciona, probar:
python --version
python3 --version
```

### Error: "Módulo no encontrado"
```bash
# Verificar que estás en el directorio correcto
pwd

# Verificar que el entorno virtual está activado
# Deberías ver (venv) al inicio de tu línea de comando
```

### Error de imports
```bash
# Asegúrate de que todos los archivos estén en el mismo directorio
# Los imports son relativos al directorio actual
```

## Próximas Funcionalidades

- [ ] Sistema de citas médicas
- [ ] Registro de diagnósticos
- [ ] Sistema de facturación
- [ ] Historial clínico de pacientes
- [ ] Gestión de consultorios médicos
- [ ] Sistema de turnos para enfermeras

## Contribuir

1. **Fork** el proyecto
2. **Clone** tu fork
3. **Crea** una rama para tu feature
4. **Commit** tus cambios
5. **Push** a tu rama
6. **Crea** un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para detalles.

## Autores

- **Tu Nombre** - [@tu-usuario](https://github.com/tu-usuario)
- **Tu Compañero** - [@compañero-usuario](https://github.com/compañero-usuario)

## Agradecimientos

- Profesor [Nombre] por la guía en POO
- Compañeros de clase por la colaboración
- Comunidad de Python por recursos y documentación

## Contacto

- **Email**: tu-email@ejemplo.com
- **GitHub**: [@tu-usuario](https://github.com/tu-usuario)
- **Issues**: [Crear issue](https://github.com/tu-usuario/trabajo-entrega-punto-7/issues)

---

**Nota**: Este README debe actualizarse conforme el proyecto evolucione. Mantén la documentación actualizada para facilitar la colaboración y revisión del compañero QA.
