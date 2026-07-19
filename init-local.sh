#!/usr/bin/env bash

set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
  echo "No se encontró .venv. Créalo e instala dependencias con:"
  echo "python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  exit 1
fi

if ! .venv/bin/python -c 'import sys; assert sys.version_info >= (3, 13)' >/dev/null 2>&1; then
  echo "El entorno .venv debe usar Python 3.13 o superior. Recrea el entorno con:"
  echo "rm -rf .venv"
  echo "python3 -m venv .venv"
  echo ".venv/bin/python -m pip install -r requirements.txt"
  exit 1
fi

if ! .venv/bin/python -c 'import email_validator, google.auth, fastapi, uvicorn' >/dev/null 2>&1; then
  echo "Faltan dependencias en .venv. Instálalas con:"
  echo ".venv/bin/python -m pip install -r requirements.txt"
  exit 1
fi

# Google Sheets usa las Application Default Credentials configuradas con gcloud.
export GOOGLE_SHEET_ID="1iQ6NhVBFmpSMx9SkWsisSj77v1lBBfAcOVuZwuvYEwY"
export GOOGLE_SHEET_RANGE="A:Z"

# Configuración exclusiva de desarrollo. Mailpit captura los correos localmente.
export DEVELOPMENT_MODE="true"
export SMTP_HOST="localhost"
export SMTP_PORT="1025"
export SMTP_FROM="FODEC <no-reply@fodec.local>"
export SMTP_STARTTLS="false"
unset SMTP_USERNAME SMTP_PASSWORD

# Se genera al iniciar si no se suministra uno. Los OTP previos quedan inválidos
# después de reiniciar el servidor, comportamiento adecuado para desarrollo.
if [[ -z "${OTP_SECRET:-}" ]]; then
  export OTP_SECRET="$(openssl rand -hex 32)"
fi

echo "Iniciando FODEC API en http://localhost:8000"
echo "Mailpit debe estar disponible en http://localhost:8025"

exec .venv/bin/python -m uvicorn app.main:app --reload
