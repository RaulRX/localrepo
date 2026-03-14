# FastAPI Greeting Service

API REST construida con FastAPI para gestionar saludos con validaciones Pydantic personalizadas.

## Estructura del Proyecto

```
src/web/fastapi/
├── config/
│   ├── Properties.py          # Gestión de configuración por entorno
│   └── resources/
│       ├── application-standalone.ini   # Config local
│       └── application-dev.ini          # Config desarrollo
├── controller/
│   ├── main.py               # Aplicación FastAPI y endpoints
│   ├── requests/
│   │   └── Greeting_request.py  # Modelos Pydantic con validaciones
│   └── responses/
│       └── Greeting_response.py # Enums de status code y response models
└── logger/
    └── Logger.py             # Logger personalizado basado en logging
```

## Configuración

### Variables de Entorno (.env)

```
environment=DEV
PYTHONPATH=.
```

**Entornos disponibles:**
- `LOCAL` - Configuración standalone
- `DEV` - Configuración de desarrollo
- `BETA` - Pre-producción
- `PRO` - Producción

### Configuración de Logger

En `resources/application-*.ini`:

```ini
[DEFAULT]
logger.level = INFO
```

Niveles: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## Ejecución

### Ejecutar servidor FastAPI

```powershell
$env:PYTHONPATH = "."; ./local_env/Scripts/python -m uvicorn src.web.fastapi.controller.main:app --reload --port 9080 --log-level debug
```

Servidor disponible en: `http://127.0.0.1:9080`

## API Endpoints

### GET /api/v1/greeting/{name}

Saluda a una persona por nombre.

**Parámetros:**
- `name` (path): Nombre de la persona
- `detail` (query, opcional): Detalle adicional

**Ejemplo:**
```
GET /api/v1/greeting/Juan?detail=developer

Respuesta: {"msg": "Hello, Juan, developer!!"}
```

### GET /api/v1/greeting

Retorna respuesta con status code.

**Respuesta:**
```json
{
  "status_code": 400,
  "message": "You've not send anything!!!"
}
```

### POST /api/v1/greeting

Crea un saludo con validaciones.

**Request body:**
```json
{
  "firstName": "Juan",
  "lastName": "Pérez",
  "description": "Desarrollador Python"
}
```

**Campos Greeting_request:**
- `firstName`: string, alias de `name`, 0-16 caracteres, default "world"
- `lastName`: string, alias de `surname`, 0-64 caracteres, obligatorio
  - Valida que contenga al menos una vocal
- `description`: string opcional, alias de `detail`, 0-255 caracteres

**Respuesta:**
```json
{
  "msg": "Hello Juan Pérez, Desarrollador Python"
}
```

## Validaciones

El modelo `Greeting_request` implementa validaciones en tres fases:

1. **`@model_validator(mode='before')`**: Normalización de entrada (trim, validación de tipos)
2. **`@field_validator`**: Validación por campo (ej: vocal en lastName)
3. **`@model_validator(mode='after')`**: Validaciones de negocio entre campos

## Enums de Status

En `Greeting_response.py`:

```python
class Status(Enum):
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    ERROR = 500

    def get_value(self) -> int:
        return self.value
```

Uso: `Status.OK.get_value()` → `200`

## Documentación Interactiva

- **Swagger UI**: http://127.0.0.1:9080/v1/swagger-ui.html
- **ReDoc**: http://127.0.0.1:9080/redoc

## Componentes Principales

### Logger.py

Logger personalizado que hereda de `logging.Logger` y carga configuración desde `Properties.py`:

```python
logger = Logger("main")
logger.debug("Debug message")
logger.info("Info message")
```

### Properties.py

Gestiona la lectura de configuración por entorno:

- Detecta variable `environment`
- Carga archivo `.ini` correspondiente
- Proporciona método `get_property(name)`

### Greeting_request.py

Modelo Pydantic con:
- Aliases para nombres de campos
- Validaciones de modelo (`before` y `after`)
- Validaciones de campo (vowel check en surname)
- Normalización automática de datos

## Alias de Campos

Los campos Pydantic usan alias para aceptar nombres en camelCase:

```python
"firstName" (alias) → "name" (atributo interno)
"lastName" (alias) → "surname"
"description" (alias) → "detail"
```

El JSON de entrada usa los alias, internamente usa los nombres de atributo.
