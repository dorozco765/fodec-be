from __future__ import annotations

import os
from dataclasses import dataclass


DEFAULT_SHEET_ID = "1iQ6NhVBFmpSMx9SkWsisSj77v1lBBfAcOVuZwuvYEwY"


@dataclass(frozen=True)
class Settings:
    google_sheet_id: str
    google_sheet_range: str
    otp_secret: str
    otp_ttl_seconds: int
    smtp_host: str | None
    smtp_port: int
    smtp_username: str | None
    smtp_password: str | None
    smtp_from: str | None
    smtp_starttls: bool
    development_mode: bool

    @classmethod
    def from_environment(cls) -> "Settings":
        ttl = int(os.getenv("OTP_TTL_SECONDS", "600"))
        if ttl <= 0:
            raise ValueError("OTP_TTL_SECONDS debe ser mayor que cero")

        return cls(
            google_sheet_id=os.getenv("GOOGLE_SHEET_ID", DEFAULT_SHEET_ID),
            google_sheet_range=os.getenv("GOOGLE_SHEET_RANGE", "A:Z"),
            otp_secret=os.getenv("OTP_SECRET", ""),
            otp_ttl_seconds=ttl,
            smtp_host=os.getenv("SMTP_HOST"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_username=os.getenv("SMTP_USERNAME"),
            smtp_password=os.getenv("SMTP_PASSWORD"),
            smtp_from=os.getenv("SMTP_FROM"),
            smtp_starttls=os.getenv("SMTP_STARTTLS", "true").lower() == "true",
            development_mode=os.getenv("DEVELOPMENT_MODE", "false").lower() == "true",
        )
