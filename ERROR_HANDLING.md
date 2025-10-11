# Manejo de Errores Mejorado - API Hospitalaria

## Descripción

Se ha implementado un sistema de manejo de errores mejorado que proporciona respuestas más descriptivas y útiles para el usuario, siguiendo las mejores prácticas de APIs REST.

## Estructura de Respuesta de Error

### Formato Estándar
```json
{
  "error_type": "TIPO_DE_ERROR",
  "message": "Mensaje descriptivo del error",
  "success": false,
  "details": {
    "field": "campo_específico",
    "value": "valor_problemático",
    "resource": "recurso_afectado"
  }
}
```

## Tipos de Errores Implementados

### 1. VALIDATION_ERROR (400)
**Cuándo se usa:** Errores de validación de datos de entrada
**Ejemplo:**
```json
{
  "error_type": "VALIDATION_ERROR",
  "message": "La contraseña debe tener al menos 8 caracteres",
  "success": false,
  "details": {
    "field": "contraseña",
    "value": "123"
  }
}
```

### 2. NOT_FOUND (404)
**Cuándo se usa:** Recurso no encontrado
**Ejemplo:**
```json
{
  "error_type": "NOT_FOUND",
  "message": "Usuario no encontrado",
  "success": false,
  "details": {
    "resource": "Usuario",
    "identifier": "123e4567-e89b-12d3-a456-426614174000"
  }
}
```

### 3. DUPLICATE_ERROR (409)
**Cuándo se usa:** Intento de crear un recurso duplicado
**Ejemplo:**
```json
{
  "error_type": "DUPLICATE_ERROR",
  "message": "Ya existe un usuario con nombre de usuario: jperez",
  "success": false,
  "details": {
    "field": "nombre de usuario",
    "value": "jperez"
  }
}
```

### 4. AUTHENTICATION_ERROR (401)
**Cuándo se usa:** Errores de autenticación
**Ejemplo:**
```json
{
  "error_type": "AUTHENTICATION_ERROR",
  "message": "Credenciales incorrectas o usuario inactivo",
  "success": false
}
```

### 5. AUTHORIZATION_ERROR (403)
**Cuándo se usa:** Usuario no tiene permisos
**Ejemplo:**
```json
{
  "error_type": "AUTHORIZATION_ERROR",
  "message": "No tiene permisos para realizar esta acción",
  "success": false
}
```

### 6. BUSINESS_LOGIC_ERROR (422)
**Cuándo se usa:** Errores de lógica de negocio
**Ejemplo:**
```json
{
  "error_type": "BUSINESS_LOGIC_ERROR",
  "message": "No se puede eliminar un médico con citas pendientes",
  "success": false,
  "details": {
    "citas_pendientes": 3
  }
}
```

### 7. SERVER_ERROR (500)
**Cuándo se usa:** Errores internos del servidor
**Ejemplo:**
```json
{
  "error_type": "SERVER_ERROR",
  "message": "Error interno al crear usuario",
  "success": false,
  "details": {
    "original_error": "Connection timeout"
  }
}
```

## Endpoints Actualizados

### ✅ Usuarios
- `POST /usuarios/` - Crear usuario
- `PUT /usuarios/{usuario_id}` - Actualizar usuario

### ✅ Autenticación
- `POST /auth/login` - Login de usuario

## Beneficios del Nuevo Sistema

1. **Claridad:** Los usuarios saben exactamente qué tipo de error ocurrió
2. **Debugging:** Los desarrolladores pueden identificar rápidamente el problema
3. **Consistencia:** Todos los errores siguen el mismo formato
4. **Información Contextual:** Los detalles adicionales ayudan a resolver el problema
5. **Códigos HTTP Apropiados:** Cada tipo de error usa el código HTTP correcto

## Uso en el Frontend

El frontend puede manejar los errores de manera más inteligente:

```javascript
try {
  const response = await fetch('/api/usuarios/', {
    method: 'POST',
    body: JSON.stringify(userData)
  });
  
  if (!response.ok) {
    const error = await response.json();
    
    switch (error.error_type) {
      case 'VALIDATION_ERROR':
        showFieldError(error.details.field, error.message);
        break;
      case 'DUPLICATE_ERROR':
        showDuplicateError(error.details.field, error.details.value);
        break;
      case 'NOT_FOUND':
        showNotFoundError(error.details.resource);
        break;
      default:
        showGenericError(error.message);
    }
  }
} catch (error) {
  console.error('Error de red:', error);
}
```

## Próximos Pasos

1. Aplicar el mismo patrón a todos los endpoints restantes
2. Agregar validaciones específicas por campo
3. Implementar logging de errores para monitoreo
4. Crear tests unitarios para el manejo de errores
