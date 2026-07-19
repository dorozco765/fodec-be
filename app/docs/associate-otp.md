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

La hoja no es pública. Habilitar **Google Sheets API** en `fodec-coop` y compartir la hoja con el correo de la cuenta de servicio de Cloud Run con permiso de lector. En Cloud Run se usa la identidad de la cuenta de servicio. Localmente, configure Application Default Credentials (ADC) con un cliente OAuth de escritorio y `gcloud auth application-default login --client-id-file=CLIENTE.json --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/spreadsheets.readonly`.

La primera fila debe contener las columnas de identificación, correo y saldo. Se aceptan los encabezados: `Identificación`/`Cédula`/`ID`, `Correo`/`Email`/`Mail`, y `Saldo`/`Saldo total`/`Aportes`. Use `GOOGLE_SHEET_RANGE` si la tabla no está en el rango `A:Z` (por ejemplo, `Asociados!A:Z`).

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

## Pruebas locales con Mailpit

Mailpit es un servidor SMTP local que captura correos sin enviarlos a Internet. Debe usarse únicamente en desarrollo.

En una terminal, iniciar Mailpit con Docker:

```bash
docker run --rm --name fodec-mailpit \
  -p 1025:1025 \
  -p 8025:8025 \
  axllent/mailpit
```

En otra terminal, desde la raíz del proyecto, iniciar la API:

```bash
./init-local.sh
```

El script configura automáticamente `SMTP_HOST=localhost`, `SMTP_PORT=1025`, `SMTP_STARTTLS=false` y `DEVELOPMENT_MODE=true`. La API queda disponible en `http://localhost:8000` y los correos capturados se consultan en `http://localhost:8025`.

Para probar el flujo completo:

1. Solicite el OTP con `POST /api/associates/otp` usando una identificación y correo que coincidan con la Sheet.
2. Abra Mailpit y copie el código de seis dígitos del mensaje capturado.
3. Envíe el código en `POST /api/associates/balance`.

Detenga Mailpit con `Ctrl+C`. Al usar `--rm`, Docker elimina automáticamente el contenedor al detenerlo.
