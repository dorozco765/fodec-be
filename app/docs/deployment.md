# Despliegue

## Proyecto

**FODEC Backend**

---

# Objetivo

Este documento describe el procedimiento oficial para desplegar el backend de FODEC en Google Cloud.

Todo despliegue deberá seguir este procedimiento para garantizar consistencia entre los entornos local y productivo.

---

# Arquitectura de Despliegue

```text
Código Fuente
      │
      ▼
Docker
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

La misma imagen Docker utilizada localmente será ejecutada en producción.

---

# Requisitos

Antes de desplegar verificar que se encuentren instalados:

* Docker Desktop
* Google Cloud SDK

---

# Verificación del entorno

## Usuario autenticado

```bash
gcloud auth list
```

Verificar que la cuenta activa sea la utilizada para administrar el proyecto.

---

## Proyecto activo

```bash
gcloud config get-value project
```

Resultado esperado

```text
fodec-coop
```

---

## Región

```bash
gcloud config get-value run/region
```

Resultado esperado

```text
us-central1
```

Si aún no está configurada

```bash
gcloud config set run/region us-central1
```

---

## Facturación

```bash
gcloud beta billing projects describe fodec-coop
```

Debe aparecer

```text
billingEnabled: true
```

---

## Servicios habilitados

```bash
gcloud services list --enabled
```

Verificar la presencia de:

* run.googleapis.com
* cloudbuild.googleapis.com
* artifactregistry.googleapis.com

---

# Docker

Construir la imagen

```bash
docker build -t fodec-api .
```

Verificar imágenes

```bash
docker images
```

Ejecutar localmente

```bash
docker run -p 8080:8080 fodec-api
```

Verificar

```text
http://localhost:8080/api/hello
```

La API debe responder correctamente antes de iniciar cualquier despliegue.

---

# Cloud Build

> **Estado actual:** Pendiente de implementación.

Los comandos oficiales se documentarán una vez se complete el primer despliegue exitoso.

---

# Artifact Registry

> **Estado actual:** Pendiente de implementación.

La creación del repositorio y la estrategia de versionado se documentarán cuando se complete la primera publicación de imágenes.

---

# Cloud Run

> **Estado actual:** Pendiente de implementación.

Después del primer despliegue se documentarán:

* Servicio
* Región
* Variables de entorno
* Configuración de CPU
* Memoria
* Escalamiento
* URL pública

---

# Validaciones posteriores al despliegue

Después de publicar una nueva versión deberá verificarse:

* El servicio responde correctamente.
* El endpoint `/api/hello` retorna HTTP 200.
* El frontend puede consumir la API.
* No existen errores en Cloud Run.
* No existen errores en Cloud Logging.

---

# Estrategia de despliegue

Durante la primera etapa del proyecto el despliegue será manual.

El flujo oficial será:

1. Validar entorno.
2. Construir la imagen Docker.
3. Verificar la imagen localmente.
4. Publicar la imagen.
5. Desplegar en Cloud Run.
6. Ejecutar pruebas funcionales.
7. Confirmar el correcto funcionamiento del frontend.

---

# Buenas prácticas

Antes de cada despliegue:

* Confirmar que la rama local se encuentra actualizada.
* Ejecutar la aplicación localmente.
* Verificar que Docker funciona correctamente.
* Confirmar el proyecto activo en Google Cloud.
* Revisar que no existan credenciales en el código fuente.

---

# Solución de problemas

## Docker no inicia

Verificar:

```bash
docker info
```

---

## Proyecto incorrecto

```bash
gcloud config set project fodec-coop
```

---

## Región incorrecta

```bash
gcloud config set run/region us-central1
```

---

## No autenticado

```bash
gcloud auth login
```

---

# Estado del proyecto

## Completado

* FastAPI
* Docker
* React
* Firebase Hosting
* Proyecto en Google Cloud
* Facturación
* Presupuesto
* Servicios habilitados

## Pendiente

* Artifact Registry
* Cloud Build
* Cloud Run
* Integración Frontend ↔ Backend

Este documento deberá actualizarse inmediatamente después del primer despliegue exitoso a Cloud Run para incorporar los comandos oficiales y la configuración definitiva de la infraestructura.
