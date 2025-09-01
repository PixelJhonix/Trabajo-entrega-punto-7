# Sistema Hospitalario - Hospital Los Enanos

Sistema de gestión hospitalaria completo desarrollado en Python con programación orientada a objetos, validaciones robustas usando Pydantic y manejo de errores mejorado.

## Descripción del Proyecto

El Sistema Hospitalario - Hospital Los Enanos es una aplicación de gestión integral para centros médicos que permite administrar pacientes, médicos, enfermeras, citas médicas, diagnósticos y facturación. El sistema está desarrollado siguiendo las mejores prácticas de programación orientada a objetos y utiliza validaciones robustas para garantizar la integridad de los datos.

## Características Principales

### Gestión de Personas
- **Pacientes**: Registro, edición y gestión completa de pacientes
- **Médicos**: Gestión de médicos con especialidades y funcionalidades específicas
- **Enfermeras**: Administración de enfermeras con turnos de trabajo

### Gestión de Citas
- Agendar citas entre médicos y pacientes
- Verificar disponibilidad de horarios automáticamente
- Cancelar y reprogramar citas
- Consultar citas por fecha, médico o paciente
- Validación de conflictos de horario

### Registro de Diagnósticos (Solo Médicos)
- Los médicos pueden registrar diagnósticos completos
- Incluye síntomas, diagnóstico, tratamiento y observaciones
- Historial completo de diagnósticos por paciente y médico
- Validaciones de formato y contenido

### Emisión de Facturas
- **Médicos**: Facturas por consultas, procedimientos y exámenes
- **Enfermeras**: Facturas por servicios de enfermería, terapias y medicamentos
- Números de factura únicos generados automáticamente
- Validaciones de montos y fechas

## Requisitos del Sistema

### Requisitos Mínimos
- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Memoria RAM**: 512 MB mínimo
- **Espacio en Disco**: 50 MB libre

### Dependencias Principales
```
pydantic>=2.0.0
typing-extensions>=4.0.0
```

## Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/sistema-hospitalario.git
cd sistema-hospitalario
```

### 2. Configurar el Entorno Virtual
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install pydantic
```

### 4. Ejecutar el Sistema
```bash
python main.py
```

## Estructura del Proyecto

```
sistema-hospitalario/
├── main.py                 # Sistema principal con menús interactivos
├── persona.py              # Clase base abstracta para todas las personas
├── paciente.py             # Clase para gestión de pacientes
├── medico.py               # Clase para gestión de médicos
├── enfermera.py            # Clase para gestión de enfermeras
├── cita.py                 # Clase para gestión de citas médicas
├── schemas.py              # Esquemas de validación con Pydantic
├── README.md               # Documentación del proyecto
└── requirements.txt        # Dependencias del proyecto
```

## Arquitectura del Software

### Diagrama de Clases

```
Persona (Abstracta)
├── Paciente
│   ├── _citas: List[Cita]
│   ├── _diagnosticos: List[Diagnostico]
│   └── _facturas: List[Factura]
├── Medico
│   ├── _especialidad: str
│   ├── _citas: List[Cita]
│   ├── _diagnosticos: List[Diagnostico]
│   └── _facturas: List[Factura]
└── Enfermera
    ├── _turno: str
    └── _facturas: List[Factura]

Cita
├── paciente: Paciente
├── medico: Medico
├── fecha: str
├── hora: str
└── motivo: str

Diagnostico
├── paciente: Paciente
├── medico: Medico
├── sintomas: str
├── diagnostico: str
└── tratamiento: str

Factura
├── paciente: Paciente
├── profesional: Union[Medico, Enfermera]
├── concepto: str
├── monto: float
└── tipo_servicio: TipoServicio
```

### Principios de Diseño Aplicados

1. **Herencia**: Todas las personas heredan de la clase base `Persona`
2. **Encapsulación**: Atributos privados con métodos públicos para acceso
3. **Polimorfismo**: Métodos comunes implementados de forma específica
4. **Composición**: Relaciones entre objetos (citas, diagnósticos, facturas)
5. **Separación de Responsabilidades**: Cada clase tiene una responsabilidad específica

## Funcionalidades Detalladas

### 1. Gestión de Pacientes

**Clase `Paciente`**
- Registro de pacientes con validación de datos
- Gestión de citas médicas
- Historial de diagnósticos y facturas

**Métodos Principales:**
- `registrar()`: Registro interactivo con validaciones
- `agendar_cita()`: Agenda citas con médicos
- `ver_citas()`: Muestra todas las citas del paciente
- `cancelar_cita()`: Cancela citas específicas

### 2. Gestión de Médicos

**Clase `Medico`**
- Registro de médicos con especialidades
- Gestión de citas y diagnósticos
- Emisión de facturas médicas

**Métodos Principales:**
- `registrar_diagnostico()`: Registra diagnósticos para pacientes
- `emitir_factura()`: Emite facturas por servicios médicos
- `agendar_cita_paciente()`: Agenda citas para pacientes
- `ver_diagnosticos()`: Muestra historial de diagnósticos

### 3. Gestión de Enfermeras

**Clase `Enfermera`**
- Registro de enfermeras con turnos
- Emisión de facturas de enfermería

**Métodos Principales:**
- `emitir_factura()`: Emite facturas por servicios de enfermería
- `ver_facturas()`: Muestra historial de facturas emitidas

### 4. Gestión de Citas

**Clase `Cita`**
- Creación y gestión de citas
- Verificación de disponibilidad
- Estados de cita (Agendada, Cancelada, Completada)

**Métodos Principales:**
- `verificar_disponibilidad()`: Verifica disponibilidad de médicos
- `verificar_disponibilidad_paciente()`: Verifica disponibilidad de pacientes
- `cancelar()`: Cancela una cita
- `completar()`: Marca una cita como completada

## Validaciones y Manejo de Errores

### Esquemas de Validación (Pydantic)

**`PersonaIn` - Validación Base**
- Nombres: Solo letras, espacios, puntos, guiones y apóstrofes
- Fechas: Formato dd/mm/yyyy con validación de fechas futuras
- Teléfonos: Formato válido con regex (7-15 dígitos)
- Direcciones: Mínimos y máximos para todos los campos

**`DiagnosticoIn` - Validación de Diagnósticos**
- Síntomas: Mínimo 10, máximo 500 caracteres
- Diagnóstico: Mínimo 5, máximo 200 caracteres
- Tratamiento: Mínimo 10, máximo 500 caracteres
- Fecha: Formato dd/mm/yyyy, no futura

**`FacturaIn` - Validación de Facturas**
- Concepto: Mínimo 5, máximo 100 caracteres
- Monto: Positivo, máximo 2 decimales, límite superior
- Tipo de servicio: Enum predefinido
- Fecha: Formato dd/mm/yyyy, no futura

### Tipos de Validaciones Implementadas

1. **Nombres**: Solo letras, espacios, puntos, guiones y apóstrofes
2. **Fechas**: Formato dd/mm/yyyy con validación de fechas futuras
3. **Teléfonos**: Formato válido con regex (7-15 dígitos)
4. **Montos**: Positivos, máximo 2 decimales, límite superior
5. **Longitudes**: Mínimos y máximos para todos los campos
6. **Enums**: Tipos de servicio y turnos predefinidos

### Manejo de Errores Mejorado

**Características del Sistema de Validación**
- Mensajes de error claros en español
- Ejemplos de formato correcto
- Guía específica para cada tipo de error
- Bucle de reintento automático
- Validación en tiempo real

## Uso del Sistema

### Ejecutar el Sistema Principal
```bash
python main.py
```

### Menú Principal
```
========================================
         MENÚ PRINCIPAL
========================================
1. Registro
2. Citas
3. Facturas
4. Diagnóstico
0. Salir
========================================
```

### Submenús Disponibles

#### 1. Registro
- Registrar Paciente
- Registrar Médico
- Registrar Enfermera
- Ver Personas Registradas

#### 2. Citas
- Agendar Cita (Paciente)
- Agendar Cita (Médico)
- Ver Citas de Paciente
- Ver Citas de Médico
- Cancelar Cita

#### 3. Facturas
- Emitir Factura por Consulta Médica
- Emitir Factura por Servicio de Enfermería
- Ver Facturas de Paciente
- Ver Facturas por Profesional

#### 4. Diagnóstico
- Registrar Diagnóstico
- Ver Historial de Diagnósticos
- Buscar Diagnósticos por Paciente
- Buscar Diagnósticos por Médico

## Ejemplos de Uso

### 1. Registrar un Paciente
```python
# El sistema solicitará los datos interactivamente
paciente = Paciente.registrar()

# Ejemplo de datos válidos:
# Nombre: María José García
# Fecha de nacimiento: 15/03/1990
# Teléfono: 555-1234
# Dirección: Calle Principal 123
```

### 2. Registrar un Médico
```python
# El sistema solicitará los datos interactivamente
medico = Medico.registrar()

# Ejemplo de datos válidos:
# Nombre: Dr. Juan Carlos López
# Fecha de nacimiento: 20/07/1975
# Teléfono: 555-5678
# Dirección: Av. Médica 456
# Especialidad: Cardiología
```

### 3. Agendar una Cita
```python
# El paciente agenda una cita con el médico
cita = paciente.agendar_cita(
    medico=medico,
    fecha="20/12/2024",
    hora="14:30",
    motivo="Consulta de control cardiológico"
)
```

### 4. Registrar un Diagnóstico
```python
# El médico registra un diagnóstico
diagnostico = medico.registrar_diagnostico(
    paciente=paciente,
    sintomas="Dolor en el pecho, dificultad para respirar, fatiga",
    diagnostico="Angina de pecho",
    tratamiento="Nitroglicerina sublingual, reposo, dieta baja en grasas",
    observaciones="Paciente debe evitar esfuerzos físicos intensos",
    fecha_diagnostico="20/12/2024"
)
```

### 5. Emitir una Factura
```python
# El médico emite una factura
factura = medico.emitir_factura(
    paciente=paciente,
    concepto="Consulta cardiológica",
    monto=150.00,
    tipo_servicio="Consulta",
    fecha_servicio="20/12/2024",
    descripcion="Consulta de control cardiológico"
)
```

## API y Documentación

### Clases Principales

#### `Persona` (Clase Abstracta)
```python
class Persona(ABC):
    """
    Clase base abstracta para todas las personas en el sistema.
    
    Attributes:
        _nombre: Nombre completo de la persona
        _fecha_nac: Fecha de nacimiento
        _telefono: Número de teléfono
        _direccion: Dirección de residencia
        _tipo: Tipo de persona
    """
    
    @abstractmethod
    def obtener_info_especifica(self) -> str:
        """Método abstracto para información específica."""
        pass
```

#### `Paciente`
```python
class Paciente(Persona):
    """
    Clase para gestión de pacientes.
    
    Methods:
        registrar() -> 'Paciente': Registro interactivo
        agendar_cita() -> Cita: Agenda cita con médico
        ver_citas() -> None: Muestra citas del paciente
        cancelar_cita() -> bool: Cancela cita específica
    """
```

#### `Medico`
```python
class Medico(Persona):
    """
    Clase para gestión de médicos.
    
    Methods:
        registrar_diagnostico() -> Diagnostico: Registra diagnóstico
        emitir_factura() -> Factura: Emite factura médica
        agendar_cita_paciente() -> Cita: Agenda cita para paciente
        ver_diagnosticos() -> None: Muestra diagnósticos
    """
```

#### `Enfermera`
```python
class Enfermera(Persona):
    """
    Clase para gestión de enfermeras.
    
    Methods:
        emitir_factura() -> Factura: Emite factura de enfermería
        ver_facturas() -> None: Muestra facturas emitidas
    """
```

### Métodos de Validación

#### Validadores de Fecha
```python
@field_validator("fecha_nac")
@classmethod
def validar_fecha_nacimiento(cls, v: str) -> str:
    """
    Valida que la fecha de nacimiento sea válida y no futura.
    
    Args:
        v: Fecha a validar
        
    Returns:
        str: Fecha validada
        
    Raises:
        ValueError: Si la fecha es inválida o futura
    """
```

#### Validadores de Nombre
```python
@field_validator("nombre")
@classmethod
def validar_nombre(cls, v: str) -> str:
    """
    Valida que el nombre solo contenga caracteres permitidos.
    
    Args:
        v: Nombre a validar
        
    Returns:
        str: Nombre validado y limpiado
        
    Raises:
        ValueError: Si el nombre contiene caracteres no permitidos
    """
```

## Contribución

### Cómo Contribuir

1. **Fork** el repositorio
2. Crea una **rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un **Pull Request**

### Estándares de Código

- **PEP 8**: Seguir las convenciones de estilo de Python
- **Type Hints**: Usar anotaciones de tipo en todas las funciones
- **Docstrings**: Documentar todas las clases y métodos
- **Validaciones**: Implementar validaciones robustas con Pydantic
- **Manejo de Errores**: Usar try-except con mensajes claros

### Estructura de Commits

```
feat: agregar nueva funcionalidad de reportes
fix: corregir validación de fechas
docs: actualizar documentación de API
test: agregar pruebas para clase Paciente
refactor: reorganizar estructura de clases
```

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor

**Desarrollado para el Trabajo de Entrega Punto 7 - Sistema Hospitalario**

---

## Soporte

Si tienes alguna pregunta o necesitas ayuda:

1. **Revisa la documentación** en este README
2. **Ejecuta las pruebas** para verificar la instalación
3. **Consulta los ejemplos** de uso proporcionados
4. **Abre un issue** en el repositorio si encuentras un bug

### Comandos de Verificación

```bash
# Verificar que todo funciona correctamente
python -c "from schemas import PacienteIn; print('Esquemas cargados correctamente')"
python -c "from paciente import Paciente; print('Clases cargadas correctamente')"
python -c "from pydantic import ValidationError; print('Pydantic disponible')"
```

---

**Gracias por usar el Sistema Hospitalario - Hospital Los Enanos**
