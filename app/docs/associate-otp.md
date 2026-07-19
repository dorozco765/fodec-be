# Consulta de saldo mediante OTP

## Endpoints

`POST /api/associates/otp`

```json
{"identification": 12345678, "email": "asociado@ejemplo.com"}
```

Siempre retorna HTTP `202` y el mismo mensaje. Solo cuando identificación y correo coinciden se envía un OTP al correo registrado. Esto evita revelar si un asociado existe o cuál es su correo.

`POST /api/associates/balance`

```json
{"identification": 12345678, "otp": "123456"}
```

Con un OTP válido retorna `200` y `{ "balance": 12345.67 }`. En cualquier otro caso retorna `401` con `OTP inválido`.

## Google Sheets

La hoja no es pública. Habilitar **Google Sheets API** en `fodec-coop` y compartir la hoja con el correo de la cuenta de servicio de Cloud Run con permiso de lector. En Cloud Run se usa la identidad de la cuenta de servicio; localmente defina `GOOGLE_APPLICATION_CREDENTIALS` apuntando a un archivo de credenciales que no debe versionarse.

La primera fila debe contener las columnas de identificación, correo y saldo. Se aceptan los encabezados: `Identificación`/`Cédula`/`ID`, `Correo`/`Email`, y `Saldo`/`Saldo total`/`Aportes`. Use `GOOGLE_SHEET_RANGE` si la tabla no está en el rango `A:Z` (por ejemplo, `Asociados!A:Z`).

## Variables de entorno

| Variable | Requerida | Descripción |
| --- | --- | --- |
| `OTP_SECRET` | Sí | Secreto aleatorio compartido entre todas las instancias. Guárdelo en Secret Manager. |
| `GOOGLE_SHEET_ID` | No | Por defecto usa la hoja suministrada. |
| `GOOGLE_SHEET_RANGE` | No | Por defecto `A:Z`. |
| `OTP_TTL_SECONDS` | No | Ventana del OTP; por defecto 600 segundos. |
| `SMTP_HOST`, `SMTP_FROM` | Sí | Servidor SMTP y remitente. |
| `SMTP_PORT` | No | Por defecto 587. |
| `SMTP_USERNAME`, `SMTP_PASSWORD` | Según proveedor | Credenciales SMTP. Guárdelas en Secret Manager. |
| `SMTP_STARTTLS` | No | Por defecto `true`. |
| `DEVELOPMENT_MODE` | No | Use `true` solo localmente para añadir `[No existe]` cuando los datos no coinciden. |

El código se deriva criptográficamente de la identificación, correo registrado y una ventana de tiempo. Por ello funciona aunque Cloud Run escale a varias instancias y no se persiste ningún OTP ni dato sensible. Es válido durante la ventana actual y la inmediatamente anterior (como máximo cerca de 20 minutos con la configuración por defecto).
