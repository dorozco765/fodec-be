# FODEC Backend

Backend del portal de autoservicio para los asociados del **Fondo de Empleados FODEC**.

Este proyecto expone una API REST desarrollada en **FastAPI**, desplegada en **Google Cloud Run** y consumida por el frontend desarrollado en React.

---

# Objetivo

El propósito del proyecto es ofrecer a los asociados una plataforma segura donde puedan consultar información de su afiliación sin necesidad de autenticarse mediante usuario y contraseña.

En su primera etapa permitirá consultar:

* Fecha de ingreso al fondo.
* Total de aportes.
* Saldos pendientes.
* Información general del asociado.

La información será obtenida inicialmente desde **Google Sheets**, permitiendo mantener el flujo de trabajo actual de los administradores del fondo sin modificar sus procesos.

La arquitectura fue diseñada para que, en el futuro, Google Sheets pueda reemplazarse por una base de datos sin afectar la API ni el frontend.

---

# Arquitectura General

```text
                 React (Firebase Hosting)
                          │
                          │ HTTPS
                          ▼
                 FastAPI (Cloud Run)
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
           Services            External Clients
                │                   │
                ▼                   ▼
          Repositories      Google Sheets API
```

La aplicación sigue una arquitectura por capas para desacoplar la lógica de negocio de la infraestructura.

---

# Stack Tecnológico

## Backend

* Python 3.13
* FastAPI
* Uvicorn

## Contenedores

* Docker

## Cloud

* Google Cloud Run
* Artifact Registry
* Cloud Build

## Frontend

* React
* Vite
* Firebase Hosting

---

# Estructura del proyecto

```text
fodec-be/

├── app/
│   ├── api/
│   ├── config/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── docs/
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Requisitos

* Python 3.13 o superior
* Docker Desktop
* Google Cloud SDK (gcloud)

---

# Instalación

Crear el entorno virtual

```bash
python3 -m venv .venv
```

Activarlo

macOS / Linux

```bash
source .venv/bin/activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecutar localmente

```bash
uvicorn app.main:app --reload
```

La aplicación quedará disponible en

```
http://localhost:8000
```

---

# Docker

Construir la imagen

```bash
docker build -t fodec-api .
```

Ejecutar el contenedor

```bash
docker run -p 8080:8080 fodec-api
```

La API estará disponible en

```
http://localhost:8080
```

---

# Endpoint de prueba

```
GET /api/hello
```

Respuesta esperada

```json
{
    "name": "Daniel Orozco"
}
```

## Consulta de saldo

Los endpoints de verificación OTP y consulta de saldo están documentados en
[`docs/associate-otp.md`](docs/associate-otp.md). La hoja se consulta mediante
Google Sheets API y las credenciales de Google y SMTP se configuran únicamente
mediante variables de entorno/Secret Manager.

---

# Verificación del entorno Google Cloud

Antes de cualquier despliegue ejecutar siempre:

Verificar autenticación

```bash
gcloud auth list
```

Verificar proyecto activo

```bash
gcloud config get-value project
```

Resultado esperado

```
fodec-coop
```

Verificar región

```bash
gcloud config get-value run/region
```

Resultado esperado

```
us-central1
```

Verificar cuenta de facturación

```bash
gcloud beta billing projects describe fodec-coop
```

Debe aparecer

```
billingEnabled: true
```

---

# Servicios habilitados

El proyecto utiliza los siguientes servicios de Google Cloud:

```bash
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com
```

---

# Flujo de despliegue

El flujo oficial del proyecto será:

```text
Código Fuente
      │
      ▼
Docker Build
      │
      ▼
Cloud Build
      │
      ▼
Artifact Registry
      │
      ▼
Cloud Run
```

Todos los despliegues deberán seguir este flujo.

---

# Principios del proyecto

Este proyecto sigue las siguientes reglas de arquitectura:

* Una única instancia de FastAPI.
* Todos los endpoints deben implementarse mediante APIRouter.
* La lógica de negocio pertenece a Services.
* El acceso a datos pertenece a Repositories.
* Google Sheets es un detalle de infraestructura, nunca una dependencia de la API.
* No almacenar secretos dentro del código fuente.
* Docker es el único mecanismo oficial de ejecución y despliegue.
* Cada Sprint debe finalizar con una versión completamente funcional.
* Toda decisión importante debe documentarse mediante ADR (Architecture Decision Record).

---

# Roadmap

## Sprint 1

* Backend FastAPI
* Frontend React
* Docker
* Firebase Hosting
* Cloud Run
* Comunicación Front ↔ Backend

## Sprint 2

* Integración con Google Sheets
* Consulta por identificación y correo
* Generación de OTP
* Validación del OTP
* Consulta de aportes

## Sprint 3

* Generación de reportes
* Impresión
* Envío por correo
* Variables de entorno
* Secret Manager

---

# Documentación

La documentación técnica del proyecto se encuentra en el directorio:

```
docs/
```

Allí se documentarán:

* Arquitectura
* Despliegue
* Decisiones de arquitectura (ADR)
* Integraciones
* Operación

---

# Licencia

Proyecto privado desarrollado para el Fondo de Empleados FODEC.
