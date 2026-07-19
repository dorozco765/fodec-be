# ADR-0005: Plataforma Cloud

**Estado:** Aceptado

## Contexto

Se requiere una plataforma con bajo costo operativo, alta disponibilidad y mínima administración.

## Decisión

El proyecto utilizará:

* Firebase Hosting para el frontend.
* Google Cloud Run para el backend.
* Artifact Registry para imágenes Docker.
* Cloud Build para la construcción de imágenes.

La región oficial será `us-central1`.

## Alternativas consideradas

Máquinas virtuales, Kubernetes, App Engine y otros proveedores cloud.

## Consecuencias

La infraestructura será administrada por Google Cloud y podrá operar dentro del nivel gratuito para el volumen esperado del proyecto.

## Revisión

Última revisión: 2026-07-19

Revisar nuevamente cuando ocurra alguno de los siguientes eventos:

- Cambio de plataforma cloud.
- Cambio de la fuente de datos.
- Incorporación de un nuevo mecanismo de autenticación.
- Reestructuración de la arquitectura.
