from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re
import unicodedata
from typing import Protocol

import google.auth
from googleapiclient.discovery import build


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(character for character in value if not unicodedata.combining(character))
    return " ".join(value.strip().lower().split())


def normalize_identification(value: str | int) -> str:
    normalized = str(value).strip()
    if re.fullmatch(r"\d+\.0+", normalized):
        normalized = normalized.split(".", maxsplit=1)[0]
    return re.sub(r"\D", "", normalized)


def normalize_email(value: str) -> str:
    return value.strip().casefold()


def parse_balance(value: str) -> Decimal:
    cleaned = re.sub(r"[^0-9,.-]", "", value.strip())
    if "," in cleaned and "." in cleaned:
        decimal_separator = "," if cleaned.rfind(",") > cleaned.rfind(".") else "."
        thousand_separator = "." if decimal_separator == "," else ","
        cleaned = cleaned.replace(thousand_separator, "").replace(decimal_separator, ".")
    elif "," in cleaned or "." in cleaned:
        separator = "," if "," in cleaned else "."
        parts = cleaned.split(separator)
        # Un único grupo de tres dígitos suele ser separador de miles (1.000).
        if len(parts) > 2 or (len(parts) == 2 and len(parts[1]) == 3):
            cleaned = "".join(parts)
        else:
            cleaned = ".".join(parts)
    try:
        return Decimal(cleaned)
    except InvalidOperation as error:
        raise ValueError("El saldo de la hoja no tiene un formato válido") from error


@dataclass(frozen=True)
class Associate:
    identification: str
    email: str
    balance: Decimal


class AssociateRepository(Protocol):
    def find_by_identification(self, identification: int) -> Associate | None: ...


class GoogleSheetsAssociateRepository:
    """Lee asociados desde Google Sheets sin exponer ese detalle al servicio."""

    _sheets_scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    _identification_headers = {"identificacion", "cedula", "id", "documento", "numero documento"}
    _email_headers = {"correo", "correo electronico", "email", "e-mail", "mail"}
    _balance_headers = {"saldo", "saldo total", "total aportes", "aportes"}

    def __init__(self, spreadsheet_id: str, range_name: str):
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name

    def find_by_identification(self, identification: int) -> Associate | None:
        values = self._read_values()
        if not values:
            return None

        columns = self._column_indexes(values[0])
        wanted_id = normalize_identification(identification)
        for row in values[1:]:
            if len(row) <= columns["identification"]:
                continue
            if normalize_identification(row[columns["identification"]]) != wanted_id:
                continue
            try:
                return Associate(
                    identification=wanted_id,
                    email=normalize_email(row[columns["email"]]),
                    balance=parse_balance(row[columns["balance"]]),
                )
            except IndexError as error:
                raise ValueError("La fila del asociado está incompleta en Google Sheets") from error
        return None

    def _read_values(self) -> list[list[str]]:
        credentials, _ = google.auth.default(scopes=self._sheets_scopes)
        service = build("sheets", "v4", credentials=credentials, cache_discovery=False)
        response = service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.range_name,
        ).execute()
        return response.get("values", [])

    def _column_indexes(self, header_row: list[str]) -> dict[str, int]:
        normalized = [normalize_text(header) for header in header_row]

        def find_column(candidates: set[str], field: str) -> int:
            for index, header in enumerate(normalized):
                if header in candidates:
                    return index
            raise ValueError(f"No se encontró la columna de {field} en Google Sheets")

        return {
            "identification": find_column(self._identification_headers, "identificación"),
            "email": find_column(self._email_headers, "correo"),
            "balance": find_column(self._balance_headers, "saldo"),
        }
