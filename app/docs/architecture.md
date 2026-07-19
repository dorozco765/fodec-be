# Arquitectura del Sistema

## Proyecto

**FODEC Backend**

Versión: 1.0

---

# Objetivo

El backend de FODEC tiene como propósito exponer una API REST que permita a los asociados consultar información relacionada con su afiliación al Fondo de Empleados de forma segura, simple y escalable.

En la primera versión la información será obtenida desde Google Sheets para no alterar el proceso operativo actual del Fondo.

La arquitectura fue diseñada para permitir reemplazar Google Sheets por cualquier otra fuente de datos sin afectar la API pública ni el frontend.

---

# Objetivos de Diseño

El proyecto fue construido siguiendo cinco principios fundamentales.

## Simplicidad

La solución debe ser fácil de entender y mantener.

Se evitarán tecnologías innecesarias o patrones complejos cuando una solución sencilla sea suficiente.

---

## Desacoplamiento

Cada componente debe tener una única responsabilidad.

Los cambios en la infraestructura no deben afectar la lógica del negocio.

---

## Escalabilidad

Aunque actualmente el sistema atenderá aproximadamente 100 asociados, la arquitectura debe permitir crecer sin necesidad de ser reescrita.

---

## Portabilidad

Toda la aplicación debe ejecutarse exactamente igual:

* Localmente.
* Docker.
* Google Cloud Run.

---

## Mantenibilidad

El proyecto debe poder ser comprendido por cualquier desarrollador nuevo en pocas horas.

Toda decisión importante será documentada mediante ADR.

---

# Arquitectura General

```text
                      React
               Firebase Hosting
                       │
                       │ HTTPS
                       ▼
                FastAPI REST API
                  Cloud Run
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
      Services                 Infrastructure
          │                         │
          ▼                         ▼
    Repositories              External Clients
          │                         │
          └────────────┬────────────┘
                       ▼
                 Google Sheets
```

---

# Arquitectura por Capas

La aplicación está dividida en capas independientes.

Cada capa tiene una única responsabilidad.

---

## API

Ubicación

```text
app/api
```

Responsabilidades

* Definir endpoints.
* Validar parámetros.
* Convertir DTOs.
* Delegar al Service.

La API nunca debe contener reglas de negocio.

---

## Services

Ubicación

```text
app/services
```

Responsabilidades

* Contener toda la lógica del negocio.
* Coordinar diferentes repositorios.
* Aplicar reglas funcionales.

Todo cambio funcional del sistema debe comenzar aquí.

---

## Repositories

Ubicación

```text
app/repositories
```

Responsabilidades

* Obtener información.
* Persistir información.
* Ocultar el origen de los datos.

La aplicación nunca debe saber si la información proviene de:

* Google Sheets
* PostgreSQL
* Firestore
* Otro servicio

Ese detalle pertenece exclusivamente al Repository.

---

## Clients

Ubicación futura

```text
app/clients
```

Responsabilidades

Consumir servicios externos.

Ejemplos:

* Google Sheets API
* Gmail
* Twilio
* WhatsApp
* reCAPTCHA

La lógica de integración nunca debe mezclarse con la lógica del negocio.

---

## Schemas

Ubicación

```text
app/schemas
```

Responsabilidades

Definir los modelos de entrada y salida utilizando Pydantic.

---

## Config

Ubicación

```text
app/config
```

Responsabilidades

Centralizar la configuración del proyecto.

Ejemplos

* Variables de entorno
* Configuración Cloud
* Secret Manager

---

# Flujo de una consulta

Cuando un asociado consulte su información el flujo esperado será:

```text
Usuario

↓

React

↓

FastAPI

↓

AssociateService

↓

AssociateRepository

↓

Google Sheets

↓

Repository

↓

Service

↓

API

↓

React

↓

Usuario
```

La API nunca accederá directamente a Google Sheets.

---

# Flujo OTP

El mecanismo de autenticación será mediante un código temporal.

Proceso

1. El usuario ingresa identificación y correo.

2. El sistema valida que ambos correspondan al mismo asociado.

3. Se genera un código OTP de seis dígitos.

4. El código tendrá una vigencia de cinco minutos.

5. El usuario ingresa el código recibido.

6. El sistema valida el OTP.

7. Se entrega la información del asociado.

No existirá autenticación mediante usuario y contraseña.

---

# Origen de los Datos

Versión inicial

Google Sheets.

Motivación

El Fondo ya administra la información mediante hojas de cálculo.

No se pretende modificar el proceso operativo existente.

---

# Estrategia de Evolución

La arquitectura fue diseñada para permitir el siguiente cambio sin afectar el resto del sistema.

Hoy

```text
Google Sheets
```

Mañana

```text
PostgreSQL
```

El único componente que deberá cambiar será el Repository.

La API permanecerá exactamente igual.

El frontend permanecerá exactamente igual.

---

# Infraestructura

Frontend

* React
* Firebase Hosting

Backend

* FastAPI
* Cloud Run

Contenedores

* Docker

Construcción

* Cloud Build

Repositorio de imágenes

* Artifact Registry

---

# Principios de Desarrollo

Durante todo el proyecto deberán respetarse las siguientes reglas.

## Una única instancia de FastAPI

Nunca crear múltiples objetos FastAPI.

Toda funcionalidad utilizará APIRouter.

---

## Docker como única plataforma de ejecución

Toda versión debe ejecutarse correctamente mediante Docker.

El entorno local y Cloud Run deben ejecutar exactamente la misma imagen.

---

## Sin secretos en Git

Nunca almacenar

* Tokens
* Passwords
* API Keys
* Credenciales

Todos los secretos deberán obtenerse desde variables de entorno o Secret Manager.

---

## Repository Pattern obligatorio

Toda fuente de datos deberá abstraerse mediante un Repository.

---

## Services contienen la lógica

La lógica del negocio nunca pertenecerá a:

* API
* Repository
* Client

---

## Código limpio

Se priorizarán

* funciones pequeñas
* nombres descriptivos
* bajo acoplamiento
* alta cohesión

---

# Decisiones Técnicas

Las decisiones relevantes del proyecto serán documentadas mediante ADR.

Ejemplos

* Arquitectura FastAPI
* Docker
* Cloud Run
* Dependencias
* Google Sheets

---

# Roadmap Técnico

## Sprint 1

Infraestructura

* React
* Firebase
* FastAPI
* Docker
* Cloud Run

---

## Sprint 2

Integración

* Google Sheets
* OTP
* Consulta de aportes

---

## Sprint 3

Servicios

* Reportes
* PDF
* Correo electrónico

---

## Sprint 4

Evolución

* Base de datos
* Caché
* Observabilidad
* Automatización de despliegues

---

# Filosofía del Proyecto

El proyecto fue diseñado bajo un principio simple.

> Construir para reemplazar.

Cada componente deberá poder sustituirse por otro equivalente con el menor impacto posible.

La infraestructura es reemplazable.

La fuente de datos es reemplazable.

Los mecanismos de autenticación son reemplazables.

La API pública deberá permanecer estable.
