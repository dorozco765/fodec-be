# FODEC Backend

Backend del portal de consulta para asociados del Fondo de Empleados FODEC.

## Tecnologías

- Python
- FastAPI
- Uvicorn
- Docker

## Requisitos

- Python 3.13+
- Docker Desktop

## Ejecutar localmente

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

La API estará disponible en:

http://localhost:8000

## Construir la imagen Docker

```bash
docker build -t fodec-api .
```

## Ejecutar el contenedor

```bash
docker run -p 8080:8080 fodec-api
```

La API estará disponible en:

http://localhost:8080

## Endpoint de prueba

GET /api/hello

Respuesta esperada:

```json
{
  "name": "Daniel Orozco"
}
```