# ADR-0006: Gestión de Dependencias

**Estado:** Aceptado

## Contexto

Las dependencias innecesarias incrementan el tamaño de las imágenes Docker y dificultan el mantenimiento.

## Decisión

El archivo `requirements.txt` contendrá únicamente dependencias directas del proyecto.

No se incluirán dependencias transitivas generadas automáticamente por el entorno virtual.

## Alternativas consideradas

Mantener un `pip freeze` completo con todas las dependencias instaladas.

## Consecuencias

Las imágenes Docker serán más pequeñas, el proyecto será más fácil de mantener y las actualizaciones de dependencias estarán bajo control.

## Revisión

Última revisión: 2026-07-19

Revisar nuevamente cuando ocurra alguno de los siguientes eventos:

- Cambio de plataforma cloud.
- Cambio de la fuente de datos.
- Incorporación de un nuevo mecanismo de autenticación.
- Reestructuración de la arquitectura.
  