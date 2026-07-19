# ADR-0002: Arquitectura FastAPI

**Estado:** Aceptado

## Contexto

La API crecerá progresivamente incorporando nuevos módulos y endpoints.

## Decisión

La aplicación utilizará una única instancia de `FastAPI`.

Todos los endpoints deberán implementarse mediante `APIRouter`.

La lógica de negocio nunca residirá en la capa API.

## Alternativas consideradas

Crear múltiples aplicaciones FastAPI o implementar toda la lógica directamente en los endpoints.

## Consecuencias

La API permanecerá organizada, modular y preparada para incorporar nuevas funcionalidades sin afectar la estructura existente.

## Revisión

Última revisión: 2026-07-19

Revisar nuevamente cuando ocurra alguno de los siguientes eventos:

- Cambio de plataforma cloud.
- Cambio de la fuente de datos.
- Incorporación de un nuevo mecanismo de autenticación.
- Reestructuración de la arquitectura.
