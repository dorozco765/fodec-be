# ADR-0001: Principios del Proyecto

**Estado:** Aceptado

## Contexto

FODEC es un proyecto con un equipo reducido y un objetivo de largo plazo. Se requiere una arquitectura que priorice la simplicidad sin impedir la evolución futura.

## Decisión

El proyecto seguirá los siguientes principios:

* Cada Sprint debe finalizar con una versión funcional.
* La simplicidad tiene prioridad sobre la sobreingeniería.
* Toda funcionalidad debe ser desplegable.
* Las decisiones importantes deberán documentarse mediante ADR.
* Ningún cambio debe comprometer la mantenibilidad del proyecto.

## Alternativas consideradas

No documentar principios y dejar las decisiones a criterio de cada desarrollador.

## Consecuencias

Todas las contribuciones deberán respetar estos principios antes de ser incorporadas al proyecto.

## Revisión

Última revisión: 2026-07-19

Revisar nuevamente cuando ocurra alguno de los siguientes eventos:

- Cambio de plataforma cloud.
- Cambio de la fuente de datos.
- Incorporación de un nuevo mecanismo de autenticación.
- Reestructuración de la arquitectura.
