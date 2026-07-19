# ADR-0003: Repository Pattern

**Estado:** Aceptado

## Contexto

La información del Fondo se administra actualmente mediante Google Sheets, pero podría migrarse a otra fuente de datos en el futuro.

## Decisión

Toda consulta o persistencia de datos deberá realizarse mediante un Repository.

La API y los Services nunca accederán directamente a Google Sheets ni a cualquier otra fuente de datos.

## Alternativas consideradas

Consumir Google Sheets directamente desde los Services o desde los endpoints.

## Consecuencias

La fuente de datos podrá reemplazarse sin modificar la lógica del negocio ni los contratos de la API.

## Revisión

Última revisión: 2026-07-19

Revisar nuevamente cuando ocurra alguno de los siguientes eventos:

- Cambio de plataforma cloud.
- Cambio de la fuente de datos.
- Incorporación de un nuevo mecanismo de autenticación.
- Reestructuración de la arquitectura.
