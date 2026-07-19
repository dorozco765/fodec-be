# ADR-0004: Docker como mecanismo Oficial de Ejecución

**Estado:** Aceptado

## Contexto

El backend deberá ejecutarse de forma idéntica en desarrollo y producción.

## Decisión

Docker será el único mecanismo oficial para ejecutar y desplegar el backend.

Toda versión publicada deberá corresponder a una imagen Docker.

## Alternativas consideradas

Ejecutar Python directamente en producción o mantener configuraciones diferentes entre entornos.

## Consecuencias

El entorno local y Cloud Run ejecutarán exactamente la misma aplicación, reduciendo diferencias entre ambientes.

## Revisión

Última revisión: 2026-07-19

Revisar nuevamente cuando ocurra alguno de los siguientes eventos:

- Cambio de plataforma cloud.
- Cambio de la fuente de datos.
- Incorporación de un nuevo mecanismo de autenticación.
- Reestructuración de la arquitectura.
